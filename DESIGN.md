---
name: Roteiros
description: Private, static day-by-day travel itineraries — a timeline you trust on the street, beside a map that always agrees with it.
colors:
  ground: "#fbfbfa"
  surface: "#ffffff"
  ink: "#17191c"
  ink-2: "#555b63"
  ink-3: "#646a72"
  rule: "#e6e7e4"
  rule-strong: "#cfd2cd"
  accent: "#b93d0a"
  accent-soft: "#fdeee4"
  food: "#9b2343"
  place: "#2f5fa8"
  activity: "#7b4bb0"
  lodging: "#5a6470"
  transport: "#0b6a72"
  shopping: "#865600"
  event: "#a02c7c"
  money: "#2f7a4f"
  notice-bg: "#fff7e0"
  notice-ink: "#6b4d00"
  dark-ground: "#121416"
  dark-surface: "#1b1e21"
  dark-ink: "#eceeef"
  dark-ink-2: "#b4b9bf"
  dark-ink-3: "#9aa0a7"
  dark-rule: "#2a2e32"
  dark-accent: "#ff9a5c"
  dark-accent-soft: "#3a2216"
typography:
  display:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "clamp(2rem, 6vw, 2.75rem)"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.375rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.015em"
  figure:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 600
    lineHeight: 1.3
    fontFeature: "\"tnum\" 1"
  title:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "\"tnum\" 1"
  body-strong:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 600
    lineHeight: 1.4
    fontFeature: "\"tnum\" 1"
  body-sm:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.45
  meta:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.4
    fontFeature: "\"tnum\" 1"
  label:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.2
  micro:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.6875rem"
    fontWeight: 600
    lineHeight: 1.2
rounded:
  focus: "6px"
  tooltip: "8px"
  notice: "10px"
  row: "12px"
  sheet: "16px"
  pill: "999px"
  circle: "50%"
spacing:
  2xs: "2px"
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  2xl: "40px"
  3xl: "48px"
components:
  day-tab:
    backgroundColor: "transparent"
    textColor: "{colors.ink-2}"
    rounded: "8px"
    padding: "5px 0 6px"
    width: "52px"
  day-tab-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "8px"
    padding: "5px 0 6px"
    width: "52px"
  stop-pin:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.meta}"
    rounded: "{rounded.circle}"
    size: "28px"
  stop-pin-current:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.surface}"
    rounded: "{rounded.circle}"
    size: "28px"
  stop-pin-past:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink-3}"
    rounded: "{rounded.circle}"
    size: "28px"
  stop-row-active:
    backgroundColor: "{colors.accent-soft}"
    rounded: "{rounded.row}"
    padding: "8px 0 12px"
  now-tag:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.surface}"
    typography: "{typography.micro}"
    rounded: "{rounded.pill}"
    padding: "1px 7px"
  map-button-floating:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.pill}"
    padding: "12px 20px"
    height: "48px"
  map-button-back:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "10px 16px"
    height: "44px"
  placeholder-notice:
    backgroundColor: "{colors.notice-bg}"
    textColor: "{colors.notice-ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.notice}"
    padding: "10px 12px"
---

# Design System: Roteiros

## Overview

**Creative North Star: "Folha de Bolso"**

The category standard for travel itineraries, played straight and made with care: a day-by-day vertical timeline beside a live map, at the craft level of Wanderlog and Google Travel. Nothing exotic, nothing selling. It must never feel decorative, slow to read, or like a booking app. The group already decided the trip; the page's only job is to be the one reference everyone trusts, at a desk while planning and one-handed on a corner abroad.

The voice is agile and utilitarian: a street tool, dense and direct, read in a glance between metro stops. Trust is the aesthetic. It comes from exact figures (time, local cost, BRL beside it), an ordered rail of numbered stops, and a map whose pins carry the same numbers in the same shape. The world is spare: a near-white ground, ink type, hairline rules, and one signal orange, chosen to stay visible in full sun, that only ever means "you are here in the trip". Category colours live in the stop pin's stroke and icon, nowhere else. Components are soft and round (pills, circles, 12px rows), friendly to one-handed use, but never decorative: if it does not speed up a glance, it does not ship. Items sit directly on the ground along the rail; there is no card around each entry.

Density is a phone app's: compact rows, 44px tap targets, tabular numerals wherever a number appears. The physical scene sets the theme: daylight on a street means a light, high-contrast default; the same phone after dinner, on the walk back, means a true dark theme that follows the system setting.

**Key Characteristics:**
- Light by default, full dark theme via `prefers-color-scheme`; same hierarchy in both.
- One accent (orange) for current position and route; four muted category tints for icons only.
- Vertical rail with numbered circular pins, mirrored exactly on the map.
- Time state on the rail: past stops recede, the current/next stop is orange, the future is plain ink.
- Every cost: local currency, then "≈ R$" in a lighter span; one rate line per trip with its date.
- Flat in the flow; shadows only on things floating above the map or the scroll.

## Colors

A cool, near-neutral paper palette with one signal orange and four muted category tints, mirrored by a graphite dark theme.

### Primary
- **Signal Orange** (accent, dark: dark-accent): the current/next stop's pin, the "Agora"/"Próximo" tag, the map route line, the day's date line, focus rings, link hover. 5.4:1 on ground; white on orange 5.6:1.
- **Orange Wash** (accent-soft, dark: dark-accent-soft): text selection only.

### Tertiary (category tints)
- **Money Green** (money, `#2f7a4f`, dark `#7fcf9b`): the local figure of a stop's cost, nothing else.
- **Wine** (food, `#9b2343`, dark `#f08aa6`; moved off terracotta so it never reads as the accent), **Atlas Blue** (place), **Muted Violet** (activity), **Slate** (lodging), **Teal** (transport, `#0b6a72`, dark `#7fd3db`), **Ochre** (shopping, `#865600`, dark `#e6bf66`), **Magenta** (event, `#a02c7c`, dark `#f0a0d8`): only the category icon and its 0.75rem label, via a per-row `--c` variable. All clear 5.8:1 on ground. In dark mode they lift to lighter versions of the same hue (see sidecar) at ≥7:1.

### Neutral
- **Paper** (ground): page background and `theme-color`; also the knock-out behind leg icons on the rail.
- **White** (surface): pins, thumbnails' badge, map controls, the map sheet.
- **Ink** (ink): headings, times, costs, pin strokes, active tab, floating map button.
- **Graphite** (ink-2): subtitles, notes, day meta, inactive tabs, leg durations. 6.6:1.
- **Muted Slate** (ink-3): tertiary metadata only (fact labels, end times, conversions, rate line, leg rows, past stops). 5.3:1 on ground, so it is legal for small text; never lighter than this.
- **Hairline** (rule) and **Hairline Strong** (rule-strong): 1px borders, row separators, the 2px rail; rule-strong is the hover border.
- **Notice Amber** (notice-bg / notice-ink): reserved for the placeholder notice that marks sample content.

### Dark theme
dark-ground `#121416`, dark-surface `#1b1e21`, dark-ink `#eceeef`, dark-ink-2 `#b4b9bf`, dark-ink-3 `#9aa0a7` (7.0:1), dark-rule `#2a2e32`, dark-accent `#ff9a5c` (ink-on-accent uses dark-ground). Elevation in dark is surface lightness, not shadow. Map tiles get `invert(1) hue-rotate(180deg) brightness(.85) contrast(.9) saturate(.6)`, turning the day map into a night map without a second provider.

### Named Rules
**The One Orange Rule.** Orange marks where you are in the trip: the current or next stop, its pin, the route, the day's date line, focus and hover. Anything orange that does none of these is wrong.

**The Tint-Not-Fill Rule.** Category colours tint the stop pin's 1.5px stroke and its icon (filling the pin only while the stop is selected). They never fill a surface or outline a row.

**The Contrast Floor Rule.** No text below 4.5:1 on its own background, in either theme, including past-stop and placeholder states. Receding means ink-3, never opacity on small text.

## Typography

**Family:** system-ui (-apple-system, Segoe UI, Roboto, sans-serif) for everything, display included. The page should read like the phone it runs on; it loads no web fonts, which also keeps it fast on patchy connections.

**Character:** hierarchy from size and weight (400/600/700), never a second family. `font-variant-numeric: tabular-nums` is set on `body`, so every time and price aligns down the rail.

### Hierarchy (the ramp — these ten steps are the only sizes)
- **Display** (700, clamp(2rem, 6vw, 2.75rem), 1.05, −0.025em): trip title, once per page.
- **Headline** (700, 1.375rem, 1.2, −0.015em): day title, with its date line inside the same heading.
- **Figure** (600, 1.125rem): trip facts (dates, days, cost per person).
- **Title** (600, 1.0625rem, 1.3): stop name; also the header subtitle at 400 in ink-2.
- **Body** (400, 1rem, 1.5): base text.
- **Body strong** (600, 0.9375rem): stop start time and stop cost.
- **Body small** (400, 0.875rem): stop notes (max 52ch), day meta, date line (500, accent), notice, tab "Dia N" (600).
- **Meta** (400, 0.8125rem): fact labels, rate line, leg rows, map tooltips (500), pin numerals (700).
- **Label** (600, 0.75rem): category label, tab weekday, end time ("até 13:30", 400).
- **Micro** (600, 0.6875rem): the "Agora"/"Próximo" tag only.

### Named Rules
**The Tabular Rule.** Every number is tabular. Costs pair local currency with "≈ R$ …" in a lighter conversion span that never wraps away from its figure.

**The Data-Above-Heading Rule.** A line above a heading carries real data, such as the day's date. No invented kicker or eyebrow.

**The pt-BR Rule.** All copy, dates and numbers are formatted by `Intl` in pt-BR: "sáb., 14 de jun.", "€ 12,50 ≈ R$ 74". Sentence case, no all-caps, no tracking.

## Layout

**Phone (default):** one column, max 680px, 16px gutters, bottom padding 120px plus `env(safe-area-inset-bottom)` to clear the floating map button. Below 480px the row grid narrows (time 42px, gaps 10px) and thumbnails shrink to 48px.

**Desktop (≥960px):** two columns. Timeline at minmax(440px, 1fr) with 40px gutters; a sticky, full-height map at 1.25fr behind a 1px rule. From 1400px the timeline is fixed at 640px and the map takes the rest.

**Day tabs:** a sticky, horizontally scrolling strip at the top, translucent ground fill with a light backdrop blur and a hairline below; `scroll-padding-top: 72px` keeps anchored days clear of it. The tab for the day in view is active.

**Timeline row:** a four-column grid: time (52px) · rail (28px) · body (fluid) · side (auto), 12px column gap.

**Rhythm:** 40px before each day, 20px under a day head, 8/12px row padding, 4px leg rows, 24px between header blocks. Spacing tokens only; no off-scale values.

## Elevation & Depth

Flat by default. Depth in the flow comes from hairlines, white-on-paper surfaces and the tab strip's blur. A shadow means "this floats above the map or the scroll". In dark mode floating things step up to dark-surface plus a 1px dark-rule border; shadows are dropped.

### Shadow Vocabulary
- **Floating pill** (`0 6px 20px rgb(0 0 0 / .22), 0 2px 4px rgb(0 0 0 / .12)`): the mobile "Ver no mapa" button.
- **Map control** (`0 4px 14px rgb(0 0 0 / .18)`): "Lista" back button and other controls over the map.
- **Map pin** (`0 2px 6px rgb(0 0 0 / .25)`): numbered pins on the tiles.

### Named Rules
**The Float-Only Shadow Rule.** Nothing in the document flow gets a shadow.

## Shapes

Soft and round. Active rows: 12px corners. Day tabs, chips and thumbnails: 8px. Floating buttons: full pills. Pins: perfect circles with a 1.5px stroke. The mobile map sheet: 16px top corners. Borders are 1px hairlines.

The rail is a 2px solid line between stops and a dashed 3px-on/4px-off line at 55% opacity across travel legs; first and last rows trim it to their pin's centre. Past segments of the rail stay rule colour; the segment leading into the current stop is orange.

Icons: 24-grid stroke icons, 2px stroke, round caps and joins, rendered at 14–18px. One icon per category and per travel mode (a pé, metrô, ônibus, trem, carro, barco, avião).

## Components

### Day Tabs
Small calendar leaves, 52px wide, 8px corners: short weekday and month (0.6875rem, 500) around the day number (1.25rem, 700).
- **Default:** transparent, ink-2 text.
- **Hover:** surface fill, hairline border, text ink.
- **Active (`aria-current="true"`):** ink fill, surface text. Driven by the day in view.
- **Today (during the trip):** the day number turns orange, so the group can jump to today.

### Timeline Stop (signature)
A row on the rail, not a card: start time with the end time below it across a hairline, a 28px pin carrying the stop's number in the day (meta, 700) with the category as its stroke colour, stop name, cost (local figure in money green, "≈ R$" in ink-3) below the name, and on the right a 56px thumbnail (48px under 480px) that opens the stop in Google Maps. Without a photo the thumbnail shows the category icon. Tapping the row opens the stop on the map. Photo credits (Wikimedia Commons) sit in one line at the page end.
- **Future:** plain ink, white pin with ink stroke.
- **Current / next (during the trip):** orange pin with white numerals and a orange "Agora" (in progress) or "Próximo" tag. On load, this row scrolls into view.
- **Past:** name and time step down to ink-3, pin stroke rule-strong with an ink-3 icon, thumbnail greyscale. Still fully readable; never hidden.
- **Hover / active (selected from list or map):** neutral hover fill (`#ecedea`, dark `#22262a`) at 12px radius; its map pin turns orange and scales to 1.2.
- **Free / no cost:** "Grátis" in ink-2; unknown cost shows nothing rather than an invented figure.

### Next Card
During the trip only, under the title: a surface card (12px radius, hairline) with the "Agora"/"Próximo" tag, "HH:MM · Nome" (title) and the leg that gets you there (meta, ink-3). Tapping scrolls to and focuses that stop. A matching orange-outline pill ("Próximo 14:15") sits at the end of the sticky day strip, so the jump is reachable from anywhere. Both recompute every minute and when the tab returns; `?agora=AAAA-MM-DDTHH:MM` pins the clock for previewing a day.

### Travel Leg
A compact meta row between stops: mode icon in the rail on a ground knock-out, bold duration in ink-2, mode ("a pé", "de metrô"), optional label, then optional cost, all one sentence in the body column ("30 min de elétrico · Elétrico 15E · € 3,10 ≈ R$ 19"), so it wraps as text instead of splitting into a right column.


### Map
Leaflet + Esri World Street Map tiles (keyless, OpenStreetMap-based), shown unfiltered by day for a Google Maps–like read. Pins repeat the 28px numbered circle and its time states. Route: orange street path from Valhalla for walk, bus, tram and car legs (train and metro always use the straight dotted line), fetched at build time (weight 4, opacity .85); a leg whose route fails falls back to a straight orange dotted line (weight 4, dash "1 8", round caps). Tooltips "HH:MM · Nome" in meta 500, 8px corners. Zoom bottom-right. Only the current day's stops are full-strength; other days' pins drop to 40% and lose numbers.
- **Loading / offline tiles:** the map area keeps its size on a ground fill with a centred meta line ("Carregando mapa…" / "Mapa indisponível sem conexão"); the timeline never depends on the map to be usable.

### Floating Map Buttons (mobile)
"Ver no mapa": ink pill, 48px, fixed bottom-centre above the safe area, map icon, Floating pill shadow. Inside the full-screen sheet, "Lista": surface pill in the same bottom-centre spot, with Map control shadow. The sheet is a modal dialog: the list behind it is inert, focus moves to "Lista" on open and back to the stop on close. Both hidden from 960px.

### Trip Header
Title, then a row of 32px chips (8px corners): dates, trip total with its conversion, country flags, travellers (initial avatars). The total comes second so it stays on the first row on phones. Below: the rate line (meta, ink-3) and, for sample data, the placeholder notice.

**Cover (when the trip has `cover`):** the title and chips sit on a full-bleed photo of the destination (Wikimedia Commons, credited top-right in 11px white). Height `clamp(360px, 58svh, 540px)` on phones, `clamp(380px, 52vh, 500px)` beside the map. Legibility comes from two layers, not one: a progressive blur (22px, saturate 1.6) masked in from 35% down, and a gradient that is black .3 at the top for the credit, clear through the middle, then the theme's ground at 45% → 82% → 100%, so the glass is whitish in light mode, dark in dark mode, and melts into the page with no edge. The title grows to `clamp(2.5rem, 10vw, 3.75rem)` in ink; chips turn to glass (surface 55%, rule-strong hairline, 20px blur). The top scrim and the white credit are the only literals outside the palette. Parallax is page-scroll-driven CSS (`animation-timeline: scroll(root)`): the photo drifts down 38% and scales to 1.08 over the first 60svh, and the title block lifts 24px and fades over 40svh. Browsers without scroll timelines and `prefers-reduced-motion` get a still cover. The next-stop card, rate line and notice follow below the cover on the ground. Without a cover, the plain header above stands.

### Placeholder Notice
Amber 10px-radius strip with an info icon at the top of any itinerary whose data is sample content, stating plainly what is fictional. Required whenever a price, time or place is not real.

### Index List
The home page list of itineraries: full-width rows between hairlines (16px vertical padding), title (title, 600) over dates and city (body-sm, ink-2). Hover: title turns orange. Upcoming or current trips first.

## Motion
State changes only: 150–250ms, `cubic-bezier(.2, 0, 0, 1)`. Row fill, pin colour, tab state and the map sheet (250ms slide up). Map pans use Leaflet's default with `animate: false` under `prefers-reduced-motion: reduce`, where every transition drops to 0ms.

## Do's and Don'ts

### Do:
- **Do** show every cost as local currency plus "≈ R$" in a lighter span, and the exchange rate with its date once per trip.
- **Do** keep the timeline pin and the map pin identical in shape, size (28px), number and state for the same stop.
- **Do** reserve orange for the current/next stop, the route, focus and the date line, in both themes.
- **Do** keep every tap target at least 44px, even when the visible control is smaller.
- **Do** keep the timeline fully usable with the map failed or offline.
- **Do** use only the ten type steps and the spacing tokens above.

### Don't:
- **Don't** wrap timeline items in bordered or shadowed cards.
- **Don't** use category colours as fills, borders or pin colours.
- **Don't** put a shadow on anything in the document flow, or any shadow in dark mode.
- **Don't** fade small text with opacity to show it is past or secondary; use ink-3.
- **Don't** add an invented label, kicker or eyebrow above a heading.
- **Don't** show a price without its currency, or sample data without the placeholder notice.
- **Don't** load web fonts, icon fonts or a second map provider.
