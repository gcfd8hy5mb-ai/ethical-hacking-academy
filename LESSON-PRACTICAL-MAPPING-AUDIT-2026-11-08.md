# Exact Lesson-to-Practical Mapping: Internal Review
Date: 2026-11-08

## Delivered
- Replaced lesson-index round-robin practice selection in `app.js` with exact course-title + lesson-title matching.
- Added `lesson-practical-title-map-2026.json` containing 52 curated practical-exercise assignments spanning 16 existing courses.
- Verified all 52 mapped titles against published supplements (`coursework-foundations-expansion-v1.json`, `coursework-systems-redteam-v1.json`, `coursework-applied-security-v1.json`, `pc-building-track.json`).
- Verified every mapped `unitId` / `sectionId` exists in `coursework-practical-expansion-2026.json`, with no duplicate course/lesson mapping keys.
- Two loose assignments (a general computer-process lesson and Windows PowerShell inspection) were withheld pending genuinely course-specific practical exercises.
- Unmapped lessons receive a transparent link to the full practice library, **not** an arbitrary topic from their level.
- Original curriculum, lesson ID indexes, knowledge checks, examination scoring and Firebase code were not edited.
- `index.html` cache-busts `app.js` with `title-matched-practice-v42-20261108` to help Safari load the update.

## Internal validation
- 52 of 52 mappings matched existing supplement source titles exactly.
- 52 of 52 mappings reference valid practice units and sections.
- No duplicate title pairs.
- `app.js` parses successfully in an async-function syntax compilation test.
- Existing progress storage key remains `ethical-hacking-academy-progress-v1`.
- The implementation checks current course/lesson indices after asynchronous data loads, so late fetch results should not be inserted into another lesson.

## Limits
- Source matching is exact-title mapping, not peer-reviewed semantic equivalence. Some mapped exercises cover adjacent skills rather than the entire topic of their lesson.
- The main core catalog (`curriculum.json`) was not parsed in this check; mappings for existing supplement lessons were verified only. Core-only lessons may remain unmapped.
- Level 8 has no regular courses in the pathway, so its separate practical exercises remain available through the level's lab links.
- Embedded practical supplements are educational guidance; original completion can still be marked using its existing knowledge-check mechanism.
- Live acceptance testing on iPhone Safari, Home Screen PWA, and desktop has not yet been performed. No independent expert subject-matter audit is completed.

## Acceptance testing
1. Open a mapped lesson such as 'Linux permissions and least privilege' and verify its related practice section displays.
2. Open an unmapped original lesson and verify a transparent practice-library fallback instead of unrelated command instruction.
3. Rapidly navigate between mapped lessons and verify old requests do not overwrite newer lesson content.
4. Confirm original knowledge-check scoring and Mark Complete behavior, and check cloud-synced progress on another device.
5. Reopen the Home Screen PWA and verify the updated app script loads rather than an older cached version.

Status: Internal content-link and syntax checks passed; device acceptance and independent curriculum review remain outstanding.
