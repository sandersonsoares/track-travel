# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Delegated: Astro, building static pages. Each itinerary is a data file (content collection) rendered to its own page at build time, and only the map ships JavaScript, as one island. The map uses Leaflet with OpenStreetMap tiles, so it needs no API key or billing. The user asked for static pages and left the stack to me. Hosting is not decided yet.

## Users

The owner and the people travelling with them. It is a private, group tool, not a public travel guide or a client deliverable. The same itinerary gets used in two ways:

- **Before the trip, on a computer:** reading at leisure, checking costs, seeing the route on the map.
- **During the trip, on a phone:** quick checks on the street, such as what comes next, when, how much it costs and how long it takes to get there.

## Product Purpose

Static pages, one per finished itinerary, that show the trip day by day in a minimal timeline. Each entry can carry places, restaurants, outings and activities, costs, and travel time between stops. The whole itinerary can also be seen on a map.

Success means the group trusts the page as the trip's single reference, whether they are planning at a desk or standing on a corner abroad.

## Positioning

These are hand-built itineraries for a known group, not generated suggestions or a booking platform. The content is already decided and the page's job is to present it clearly. Nothing on it is selling anything.

## Operating Context

- Itineraries are written and finished ahead of time and published as static pages. There is no in-app editing.
- They are read on a phone mid-trip, possibly one-handed, outdoors and on patchy connections, and on a desktop during planning.
- Shared with travel companions by link.

## Capabilities and Constraints

- **Timeline:** minimal, ordered by day and time. Item types include places, restaurants, outings/activities and travel legs.
- **Costs:** shown in the destination's local currency with the BRL conversion beside it.
- **Travel time:** time between consecutive stops.
- **Map:** the itinerary's stops plotted on a map.
- **Language:** Portuguese (pt-BR) for all copy, dates and number formatting.
- **Undecided:**
  - the itinerary data schema;
  - the exchange-rate source and whether each page fixes the rate and its date;
  - whether pages work offline;
  - per-person cost splitting;
  - the hosting/deploy target;
  - whether pages need access control or rely on unlisted links.

## Brand Commitments

No name or brand assets yet. The user chose the category standard for the itinerary pages: a clean, conventional travel-app timeline on the level of Wanderlog and Google Travel, made with care. Those two are the craft bar.

## Evidence on Hand

None yet: no itineraries, photos or brand assets are in the project. Future work must not invent real prices, opening hours, travel times or places and present them as fact. Sample content has to be clearly marked as placeholder.

## Product Principles

1. **Next thing first.** During the trip, the answer to "what's next, when, how do I get there" should take seconds to find.
2. **Numbers you can trust.** Costs and times are shown plainly, with the currency and conversion explicit, never vague.
3. **Calm over clever.** The timeline stays minimal so the trip's content carries the page.
4. **Map and timeline are one story.** The same stops, in the same order, in both views.
5. **Static and durable.** Pages are plain, fast and shareable by link, with nothing to log into.

## Accessibility & Inclusion

Needs to be readable on a phone in bright outdoor light and usable with one hand. Map content must also be available as text (in the timeline) so it does not depend on the map alone.
