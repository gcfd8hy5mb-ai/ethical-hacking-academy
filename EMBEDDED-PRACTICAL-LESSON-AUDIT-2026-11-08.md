# Ethical Hacking Academy — Embedded Practical Lesson Integration Audit

Date: 2026-11-08
Status: Internal structural checks completed; live browser acceptance tests and independent technical review outstanding.

## What changed
- Existing lesson view now displays a lazily loaded practical extension between the core reading and the existing lesson knowledge check.
- Each extension includes a scenario, detailed explanation, command or method, interpretation guide, assignment, and authorized/safe-use boundary.
- Extensions are selected deterministically from two units and six sections associated with the current level. This is **level-matched** guidance, not a semantic guarantee of a precise match to each individual lesson topic.
- The original lesson title, reading, knowledge-check choices, answer key, completion action, course order and progress identifiers are unchanged.
- `index.html` references the updated `app.js` URL with a new query parameter to avoid reuse of an older cached script.

## Structural observations
- Updated `app.js` JavaScript parsed successfully using an async-function syntax compilation check.
- All eight levels have two units and six practical instruction sections available in `coursework-practical-expansion-2026.json`.
- The loading process fetches the supplemental catalog on lesson demand and reuses the resulting promise.
- Fetch failure displays a non-blocking fallback link, not a broken/empty knowledge check.
- Concurrent navigation guard prevents a response to an earlier lesson from replacing content after the student navigates to a different lesson.
- Level 8 has no ordinary courses in the current pathway so level 8 supplemental lessons remain reachable through the level's lab links rather than embedded into individual Level 8 lessons.
- The original Firebase cloud functions, lesson completion storage and examination grading code were not deliberately modified.

## Limitations and risk
- The supplemental guidance cycles through level sections by legacy lesson number; it is not yet individually aligned to every single lesson title. Future improvement should supply explicit per-lesson practice mappings after an authored curriculum content audit.
- The new embedded content has no separate cloud progress or independent grading; original lesson completion remains the same.
- Inline blocks are rendered from an external JSON file. A connectivity failure should not prevent original lesson reading or tests.
- Syntax and static-data checks are not a substitute for DOM event tests, mobile PWA cache verification, accessibility reviews, or academic validation.

## Acceptance testing to complete
1. On desktop and iPhone Safari, open an existing Level 1 lesson; confirm the new practice extension appears between the reading and knowledge check.
2. Switch immediately to another lesson while data loads; confirm the extension belongs to the new lesson.
3. Answer an original knowledge check; confirm grade feedback and Mark complete still function.
4. Reload and verify legacy lesson progress persists unchanged across devices where Firebase is enabled.
5. Open Level 3, 5 and 7 course lessons; confirm level-correct supplemental content is shown.
6. Disconnect from network during an already-open lesson; confirm original knowledge check remains usable and fallback renders.
7. Confirm direct Level 8 lab link still opens supplementary practice.

Sign-off: internal code and structural review only. Neither independent academic review nor on-device production acceptance sign-off has been performed.
