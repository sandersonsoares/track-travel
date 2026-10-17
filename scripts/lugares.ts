// Fills `place` on each itinerary item at build time:
//   OpenStreetMap (Overpass) → address, hours, website, phone, and the Wikidata link;
//   Wikidata → main photo + Commons category; Commons → up to MAX_PHOTOS photos with credits.
// The OSM feature is found by coordinates AND name, so generic items ("Hotel na Baixa") stay empty
// instead of borrowing a neighbour's data. If OSM has no Wikidata link, a Wikipedia article near the
// item with the same name is used instead.
// Items that already have `place` are skipped (delete it to refetch); items saved while Overpass was
// down, or added without photos yet, carry `osmPending` and are retried. A retry only fills what is
// missing: existing fields and photos are kept.
import { Glob } from 'bun';

const MAX_PHOTOS = 6;
const RADIUS_M = 200;
const OVERPASS = ['https://overpass-api.de/api/interpreter', 'https://overpass.private.coffee/api/interpreter', 'https://maps.mail.ru/osm/tools/overpass/api/interpreter'];
// Wikimedia throttles agents without a contact URL.
const UA = { 'User-Agent': 'roteiros/1.0 (https://www.mediawiki.org/wiki/API:Etiquette) bun' };

type Photo = { src: string; page: string; author?: string; license?: string };
type Place = { osmPending?: boolean; address?: string; hours?: string; website?: string; phone?: string; osm?: string; photos: Photo[] };

const words = (t: string) => t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().split(/[^a-z0-9]+/).filter((w) => w.length > 2 && !['dos', 'das', 'del', 'the'].includes(w));
// Every significant word of the item's name (before " · " or " (") must appear in the candidate's name.
const sameName = (name: string, other = '') => { const t = new Set(words(other)); const n = words(name.split(/ · | \(/)[0]); return n.length > 0 && n.every((w) => t.has(w)); };
const km = (a: number, b: number, c: number, d: number) => { const r = Math.PI / 180; return Math.hypot((d - b) * r * Math.cos(((a + c) / 2) * r), (c - a) * r) * 6371; };
const strip = (h?: string) => h?.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim() || undefined;

async function get(url: string | URL, init?: RequestInit) {
  for (let n = 0; n < 2; n++) {
    const res = await fetch(url, { ...init, headers: UA, signal: AbortSignal.timeout(30_000) }).catch(() => undefined);
    await Bun.sleep(700);
    if (res?.ok) return res.json();
    await Bun.sleep(4000 * (n + 1));
  }
  throw new Error(`falhou: ${url}`);
}
const wiki = (host: string, params: Record<string, string>) => {
  const u = new URL(`https://${host}/w/api.php`);
  Object.entries({ format: 'json', origin: '*', ...params }).forEach(([k, v]) => u.searchParams.set(k, v));
  return get(u);
};

let overpassDown = false;
async function osm(name: string, lat: number, lng: number) {
  if (overpassDown) throw new Error('Overpass indisponível');
  const q = `[out:json][timeout:25];nwr["name"](around:${RADIUS_M},${lat},${lng});out tags center;`;
  // Public Overpass servers go down often; try the mirrors in turn.
  let j: any;
  for (const host of OVERPASS) {
    j = await get(host, { method: 'POST', body: new URLSearchParams({ data: q }) }).catch(() => undefined);
    if (j) break;
  }
  if (!j) { overpassDown = true; throw new Error('Overpass indisponível'); }
  return j.elements.find((e: any) => [e.tags.name, e.tags['name:pt'], e.tags['name:en']].some((v) => sameName(name, v)));
}

async function wikidataFromWikipedia(name: string, lat: number, lng: number) {
  for (const lang of ['pt', 'en']) {
    const j = await wiki(`${lang}.wikipedia.org`, { action: 'query', generator: 'search', gsrsearch: name, gsrlimit: '5', prop: 'pageprops|coordinates', ppprop: 'wikibase_item' });
    const hit = Object.values<any>(j.query?.pages ?? {}).find((p) => p.pageprops?.wikibase_item && p.coordinates && sameName(name, p.title) && km(lat, lng, p.coordinates[0].lat, p.coordinates[0].lon) <= 1);
    if (hit) return hit.pageprops.wikibase_item as string;
  }
}

async function photos(qid: string): Promise<Photo[]> {
  const e = (await wiki('www.wikidata.org', { action: 'wbgetentities', ids: qid, props: 'claims' })).entities[qid];
  const claim = (p: string) => e?.claims?.[p]?.[0]?.mainsnak?.datavalue?.value as string | undefined;
  const main = claim('P18'), category = claim('P373');
  const titles = main ? [`File:${main}`] : [];
  if (category) {
    const j = await wiki('commons.wikimedia.org', { action: 'query', list: 'categorymembers', cmtitle: `Category:${category}`, cmtype: 'file', cmlimit: '30' });
    titles.push(...j.query.categorymembers.map((m: any) => m.title).filter((t: string) => /\.(jpe?g|png|webp)$/i.test(t)));
  }
  const pick = [...new Set(titles)].slice(0, MAX_PHOTOS);
  if (!pick.length) return [];
  const j = await wiki('commons.wikimedia.org', { action: 'query', titles: pick.join('|'), prop: 'imageinfo', iiprop: 'url|extmetadata', iiurlwidth: '640' });
  const info = new Map(Object.values<any>(j.query.pages).map((p) => [p.title, p.imageinfo?.[0]]));
  return pick.flatMap((t) => {
    const i = info.get(t);
    return i ? [{ src: i.thumburl, page: i.descriptionurl, author: strip(i.extmetadata?.Artist?.value), license: i.extmetadata?.LicenseShortName?.value }] : [];
  });
}

// Fallback for places without Wikidata (shops, restaurants): Commons photos taken within 150 m whose
// file name carries the place's name, so a busy street does not lend its photos to every shop on it.
async function nearbyPhotos(name: string, lat: number, lng: number): Promise<Photo[]> {
  const j = await wiki('commons.wikimedia.org', { action: 'query', list: 'geosearch', gscoord: `${lat}|${lng}`, gsradius: '150', gsnamespace: '6', gslimit: '50' });
  const titles = (j.query?.geosearch ?? []).map((g: any) => g.title as string).filter((t: string) => /\.(jpe?g|png|webp)$/i.test(t) && sameName(name, t.replace(/^File:/, '').replace(/[_.-]+/g, ' ')));
  const pick = titles.slice(0, MAX_PHOTOS);
  if (!pick.length) return [];
  const info = await wiki('commons.wikimedia.org', { action: 'query', titles: pick.join('|'), prop: 'imageinfo', iiprop: 'url|extmetadata', iiurlwidth: '640' });
  return Object.values<any>(info.query.pages).flatMap((pg) => {
    const i = pg.imageinfo?.[0];
    return i ? [{ src: i.thumburl, page: i.descriptionurl, author: strip(i.extmetadata?.Artist?.value), license: i.extmetadata?.LicenseShortName?.value }] : [];
  });
}

async function lookup(name: string, lat: number, lng: number): Promise<Place> {
  // Overpass down: keep going with Wikipedia photos and flag the item so the next run fills OSM data.
  const el = await osm(name, lat, lng).catch(() => null);
  const t = el?.tags ?? {};
  const street = [t['addr:street'], t['addr:housenumber']].filter(Boolean).join(', ');
  const address = [street, t['addr:city']].filter(Boolean).join(' · ') || undefined;
  const qid = t.wikidata ?? (await wikidataFromWikipedia(name, lat, lng));
  return {
    ...(el === null && { osmPending: true }),
    address,
    hours: t.opening_hours,
    website: t.website ?? t['contact:website'],
    phone: t.phone ?? t['contact:phone'],
    osm: el && `https://www.openstreetmap.org/${el.type}/${el.id}`,
    photos: await (async () => { const ph = qid ? await photos(qid) : []; return ph.length ? ph : nearbyPhotos(name, lat, lng).catch(() => []); })(),
  };
}

const seen = new Map<string, Place>();
for await (const path of new Glob('src/data/*.json').scan()) {
  const trip = await Bun.file(path).json();
  let changed = false;
  // Alternatives (item.alternatives) get the same treatment as the planned items.
  for (const day of trip.days) for (const item of day.items.flatMap((i: any) => [i, ...(i.alternatives ?? [])])) {
    if (item.place && !item.place.osmPending) continue;
    const key = `${item.name}@${item.lat},${item.lng}`;
    try {
      if (!seen.has(key)) seen.set(key, JSON.parse(JSON.stringify(await lookup(item.name, item.lat, item.lng))));
    } catch (err) {
      console.warn('!', item.name, (err as Error).message);
      continue;
    }
    // Merge instead of replace: fields already filled by hand or from Google (address, hours,
    // phone, website, instagram, googleMapsUrl…) and photos already saved are never overwritten.
    const found = seen.get(key)!;
    const kept = Object.fromEntries(Object.entries(item.place ?? {}).filter(([k, v]) => k !== 'osmPending' && v != null && v !== '' && !(Array.isArray(v) && !v.length)));
    item.place = { ...found, ...kept, photos: item.place?.photos?.length ? item.place.photos : found.photos };
    if (!found.osmPending) delete item.place.osmPending;
    changed = true;
    const p = item.place;
    console.log(p.osmPending ? '…' : p.osm ? '✓' : '·', item.name, p.photos.length ? `${p.photos.length} fotos` : '', p.address ?? '');
  }
  if (changed) await Bun.write(path, JSON.stringify(trip, null, 2) + '\n');
}
