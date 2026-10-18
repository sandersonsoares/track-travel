// Fills `place` on each itinerary item at build time:
//   OpenStreetMap (Overpass) → address, hours, website, phone, and the Wikidata link;
//   Wikidata → main photo + Commons category; Commons → up to MAX_PHOTOS photos with credits.
// The OSM feature is found by coordinates AND name, so generic items ("Hotel na Baixa") stay empty
// instead of borrowing a neighbour's data. If OSM has no Wikidata link, a Wikipedia article near the
// item with the same name is used instead.
// An item is looked up only when it has no `place`, when its name or coordinates changed since the last
// lookup (`place.lookupKey`), or when it carries `osmPending` (Overpass was down) and the last try is over
// RECHECK_MS old. Delete `place` to refetch by hand. A retry only fills what is missing: existing fields
// and photos are kept. Lookups run CONCURRENCY at a time; each host is still paced by HOST_GAP_MS.
import { Glob } from 'bun';

const MAX_PHOTOS = 6;
const RADIUS_M = 200;
const CONCURRENCY = 4;
const RECHECK_MS = 7 * 24 * 3600 * 1000;
const HOST_GAP_MS = 250;
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

// Reserves the next request slot for the host, so parallel lookups never hit one host faster than HOST_GAP_MS.
const nextSlot = new Map<string, number>();
async function throttle(url: string | URL) {
  const host = new URL(url).hostname;
  const now = Date.now();
  const at = Math.max(now, nextSlot.get(host) ?? 0);
  nextSlot.set(host, at + HOST_GAP_MS);
  if (at > now) await Bun.sleep(at - now);
}

async function get(url: string | URL, init?: RequestInit) {
  for (let n = 0; n < 2; n++) {
    await throttle(url);
    const res = await fetch(url, { ...init, headers: UA, signal: AbortSignal.timeout(30_000) }).catch(() => undefined);
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

const keyOf = (item: any) => `${item.name}@${item.lat},${item.lng}`;

function needsLookup(item: any, now: number) {
  const p = item.place;
  if (!p) return true;
  if (p.lookupKey && p.lookupKey !== keyOf(item)) return true;
  if (!p.osmPending) return false;
  return now - (p.checkedAt ? Date.parse(p.checkedAt) : 0) > RECHECK_MS;
}

async function pool<T>(xs: T[], n: number, fn: (x: T) => Promise<void>) {
  let i = 0;
  await Promise.all(Array.from({ length: Math.min(n, xs.length) }, async () => {
    while (i < xs.length) await fn(xs[i++]);
  }));
}

const now = Date.now();
const files: { path: string; trip: any; todo: any[] }[] = [];
for await (const path of new Glob('src/data/*.json').scan()) {
  const trip = await Bun.file(path).json();
  // Alternatives (item.alternatives) get the same treatment as the planned items.
  const all = trip.days.flatMap((day: any) => day.items.flatMap((i: any) => [i, ...(i.alternatives ?? [])]));
  files.push({ path, trip, todo: all.filter((item: any) => needsLookup(item, now)) });
}

// One lookup per distinct name@coordinates, shared by every item that has it.
const first = new Map<string, any>();
for (const f of files) for (const item of f.todo) if (!first.has(keyOf(item))) first.set(keyOf(item), item);
const results = new Map<string, Place | Error>();
await pool([...first.keys()], CONCURRENCY, async (key) => {
  const item = first.get(key);
  try { results.set(key, await lookup(item.name, item.lat, item.lng)); }
  catch (err) { results.set(key, err as Error); }
});

for (const { path, trip, todo } of files) {
  const due = new Set(todo);
  let changed = false;
  for (const day of trip.days) for (const item of day.items.flatMap((i: any) => [i, ...(i.alternatives ?? [])])) {
    if (!due.has(item)) {
      // Finished places from before lookupKey existed get stamped once, so later name changes are detected.
      if (item.place && !item.place.lookupKey) { item.place.lookupKey = keyOf(item); changed = true; }
      continue;
    }
    const found0 = results.get(keyOf(item))!;
    if (found0 instanceof Error) { console.warn('!', item.name, found0.message); continue; }
    const found: Place = JSON.parse(JSON.stringify(found0));
    // Merge instead of replace: fields already filled by hand or from Google (address, hours,
    // phone, website, instagram, googleMapsUrl…) and photos already saved are never overwritten.
    const kept = Object.fromEntries(Object.entries(item.place ?? {}).filter(([k, v]) => !['osmPending', 'lookupKey', 'checkedAt'].includes(k) && v != null && v !== '' && !(Array.isArray(v) && !v.length)));
    item.place = { ...found, ...kept, photos: item.place?.photos?.length ? item.place.photos : found.photos, lookupKey: keyOf(item), checkedAt: new Date().toISOString() };
    if (!found.osmPending) delete item.place.osmPending;
    changed = true;
    const p = item.place;
    console.log(p.osmPending ? '…' : p.osm ? '✓' : '·', item.name, p.photos.length ? `${p.photos.length} fotos` : '', p.address ?? '');
  }
  if (changed) await Bun.write(path, JSON.stringify(trip, null, 2) + '\n');
}
