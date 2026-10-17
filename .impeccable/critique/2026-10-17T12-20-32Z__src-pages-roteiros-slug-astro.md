---
target: critique
total_score: 26
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 2
target_identity: "file:/Users/sanderson/Documents/projects/track-travels/src/pages/roteiros/[slug].astro"
target_fingerprint: "sha256:22fac609516f81e326d17126d0210efc5ffb87bb882bddd8888500c180e3c676"
target_path: /Users/sanderson/Documents/projects/track-travels/src/pages/roteiros/[slug].astro
timestamp: 2026-10-17T12-20-32Z
slug: src-pages-roteiros-slug-astro
---
# Critique: src/pages/roteiros/[slug].astro
Method: dual-agent (A: adb4324e837fea319 · B: a2c0586efc5ec0930)
Score 26/40 (Acceptable). H1 3, H2 3, H3 3, H4 3, H5 2, H6 2, H7 2, H8 4, H9 2, H10 2.
Detector: CLI 0 findings. Browser: leaflet tile/attribution findings (false positive), .leg::before repeating gradient = intentional dashed rail (false positive), heading-rhythm on stop h3s (row structure, false positive).
## Priority issues
- [P1] Detail panel / mobile sheet covers the selected pin; pan with panel offset (focusStop). polish
- [P1] Agora/Próximo computed once at load; recompute on visibilitychange + 60s, add jump-to-next control. harden
- [P2] Train/metro legs routed as roads (Valhalla auto); use straight dashed line for rail/metro. clarify
- [P2] List not inert behind mobile map sheet; inert + role=dialog + focus move. audit
- [P3] Pins carry type icon, no number; map and list share no ordinal. polish
## Minor
Duplicate .stop.is-past .stop-thumb rule; countries?.length && renders "0"; no reduced-motion guard on flyTo/smooth scroll; mobile header pushes first stop to ~y630; "Lista" top-left out of thumb reach.
