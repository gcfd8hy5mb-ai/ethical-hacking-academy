# Ethical Hacking Academy — Curriculum and Student Journey Audit (2026-11-03)

## Audit scope and limitations
Reviewed the GitHub main-branch Academy source, learning pathway, examination catalog, 3 supplemental coursework files, separate hardware track, and practical checkpoint. No real iPhone browser session, Firebase account, full live deployment acceptance test, external academic review, or real computer exercise was performed. The large primary `curriculum.json` could not be reliably retrieved through the available repository reader, so **the total authored lesson count and total verified study hours remain unknown**. Do not imply that a 440-hour program is fully authored or externally approved.

## Verified structure
- 8 learning levels, with a combined **440-hour planning budget**, including instruction, labs, exams, revision and remediation. Level budgets: 35, 45, 75, 55, 75, 45, 75, 35 hours. These are targets, not measured reading or study durations.
- 22 examinations in `exams.json`, with an 80% pass threshold in the existing examination engine.
- 30 lessons across 3 separately appended PC-building courses.
- 18 foundation supplement lessons, 12 system-and-reporting supplement lessons, and 15 applied-security supplement lessons: **75 confirmed supplemental/hardware lessons** across these four inspected files, in addition to the original primary curriculum. No exact duplicate titles within the same course were detected among these four files. The loader also guards against exact-title duplicates when appending to an existing course.
- 8 synthetic stateful mastery checkpoint scenarios; **not** actual operating-system or hardware proficiency.
- Existing source-level lesson-progress keys, exam-result keys, and separate practical checkpoint records remain unchanged.

## Learning journey and assessments
1. Home > eight-level pathway: Levels link to their original courses and exercises. Verify live navigation on an iPhone and desktop.
2. Lesson completion: original numerical course/lesson indexes preserved by appending new lessons only. The progress total now counts only valid existing lesson references, not stale unknown saved IDs.
3. Examination pass: relevant per-course exams are reused across levels. This can result in multiple exams being displayed under a single level; avoid presenting the same exam as new study hours more than once. No exam questions or pass records were changed during this audit.
4. Practical mastery: synthetic cases remain linked to all eight levels. Students can type diagnostic commands, implement a fictional fix, verify state, and write reports. Existing achievements have not been invalidated by optional report self-review.
5. Level 8: no ordinary course/lesson IDs are assigned. Final readiness now recognizes the existing Part I and Part II qualification simulations, plus the eight practical checkpoint reports, instead of permanently waiting for an unmapped standard exam. These remain only simulated evidence requiring independent human evaluation.
6. Firebase: the app has cloud-save integration for lesson progress. Separate standalone practical checkpoint records are not confirmed to sync, so test and back them up before changing devices; do not claim that all practice progress is protected.

## Outstanding work, in priority order
- **P0 deployment validation:** On iPhone Safari and saved Home Screen app, confirm all eight level pages, course > lesson > exam navigation, Back buttons, Cloud Saving under Settings, and no stale CSS/JS caching. Repeat on desktop.
- **P0 cloud save reconciliation:** Verify cross-device lesson progress for the same authorized account; identify which standalone lab data is not included in cloud snapshots. Preserve conflict/rollback behavior.
- **P1 comprehensive course inventory:** Retrieve or locally clone `curriculum.json` through a tool that supports its full size, enumerate all courses and lesson hours, reconcile original indexes against the learning path, list unmatched courses. Current repo reader did not return the file contents; percentages based on complete authored hours must remain **unverified** until then.
- **P1 lesson-quality review:** Review each lesson for prerequisites, originality, real command syntax, environment-specific caveats, accessible explanations and assessment alignment; check conceptual overlap across the primary curriculum and supplements rather than deleting by title alone.
- **P1 reliability tests:** Create repeatable automated regression checks covering all eight practical cases (diagnosis before correction, observed successful state change, verification after repair, preserved saved data and long-form reports).
- **P1 independent practical validation:** Human-review written explanations, test permitted actions in owned isolated virtual machines, and determine whether skills transfer beyond scripted fictional outputs.
- **P2 efficiency:** Allocate the verified authored workload within the level study budgets; consolidate redundant explanations carefully without changing original lesson IDs or invalidating user progress. Prioritize exercises that teach interpretation and troubleshooting over additional repetitive quizzes.

## Acceptance boundaries
Do not renumber original courses or lessons; do not remove saved student records, reset Firebase, or modify existing exam result keys; do not imply external accreditation, academic sign-off, professional certification, or real-system mastery from synthetic simulations. Perform live tests before saying the deployed iPhone app has passed end-to-end acceptance.
