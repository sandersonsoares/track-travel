---
version: 1
slug: "src-pages-roteiros-slug-astro"
primary_target: "src/pages/roteiros/[slug].astro"
related_targets: []
---

# Página de roteiro

Scope: `src/pages/roteiros/[slug].astro` — one page per finished itinerary. Mode: Operate (consult during trip, plan before).
Audience/job: the owner and travel companions; answer "what's next, when, how much, how far" on a phone, and review the whole trip with the map on desktop.
Content: placeholder itinerary (Lisboa, 3 days), every price/time marked as example.

## Direction contract
THESIS: the canon travel-app timeline (Wanderlog / Google Travel tier), played straight and crafted: a day-by-day vertical timeline beside a live map. Refuses nothing exotic; refuses sloppiness: vague costs, map and list disagreeing.
OWN-WORLD: light, near-white ground, ink text, one deep teal accent for the active stop and route; category colors only as small icon tints (place, food, activity). System UI sans, tabular numerals. Thin rules, 12px radii, no card shells around every item.
STORY: open the link → see trip, dates, total cost → pick a day → read stops in order with time, cost (local + BRL), travel leg → tap a stop to find it on the map.
FIRST VIEWPORT: desktop: left column trip title, dates, total cost, day tabs, then timeline; right ~55% sticky map with numbered pins and route line. Mobile: title + totals, sticky day tabs, timeline; floating "Ver no mapa" button opens a full-screen map sheet.
FORM: canon (standing exit), seed 6499800f.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
