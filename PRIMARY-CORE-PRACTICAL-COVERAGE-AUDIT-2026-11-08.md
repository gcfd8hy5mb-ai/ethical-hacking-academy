# Primary Curriculum Practical Mapping — 2026-11-08

## Baseline and delivered change
- Retrieved full primary `curriculum.json` through GitHub REST contents. It contains version 36, **26 courses and 198 core lessons**.
- Added `core-lesson-guided-practice-2026.json`: 50 authored practical exercises spanning 7 core courses.
- Added 50 title-matched links to `lesson-practical-title-map-2026.json`, increasing overall core/supplement mapping entries from 75 to **125**.
- Updated `app.js` to read the pre-existing two practical catalogs plus the 50-core-lesson catalog using `Promise.allSettled` so a failed supplemental fetch does not prevent other available practice data from loading.
- Updated the app script reference in `index.html` to `core-practice-v44-20261108` for mobile/PWA cache turnover.

## Content coverage
Primary curriculum core lessons: 198.
Core lessons with exact title-based practice mapping: 50 (25.3%).
Core lessons still without mapped practice: **148**.
Other mapped entries: 75 from previously authored supplemental lessons.
Total distinct mapping entries: 125.

Core courses covered in this batch:
1. Computer and Operating-System Essentials — 6
2. Beginner Linux and Terminal Skills — 8
3. Windows Administration and Security — 8
4. Networking Practice and Troubleshooting — 8
5. Programming Logic for Security Beginners — 8
6. Security Operations and Incident Response — 6
7. Security Monitoring and Log Analysis — 6

The other 19 primary courses need detailed practical authoring. Unmapped lessons display a practice-library link rather than unrelated content.

## Internal checks
- JavaScript async module syntax: PASS.
- Exact exercise ID and section ID references: zero broken references.
- Duplicate title mapping pairs: zero.
- Cache-busting script reference in HTML: present.
- Existing original progress-key string remains in the application.
- The original core `curriculum.json`, exams and Firebase modules were not edited.

## Technical and academic limitations
- The new practice is instructional content and does not yet require objectively verified hands-on results to complete an existing lesson.
- Browser and WSL runtime testing has not been performed in this batch.
- Commands and method descriptions should be independently checked on suitable target operating systems before a student is instructed to rely on them.
- New and existing practice material is not reviewed or accredited by an external institution.
- Completion records for original lessons remain separate; passing a self-scored practice does not confer professional certification.

## Next work
1. Author specific assignments for the remaining 148 core lessons, prioritizing web security, enterprise identity, cybersecurity foundations and foundational networking.
2. Improve dynamic practice evidence capture and acceptance tests without breaking legacy lesson completion or Firebase cloud saving.
3. Add test fixtures for the Linux evidence reviewer and run them in Ubuntu/WSL 1.
4. Conduct mobile Safari, desktop browser, PWA cache and accessibility acceptance testing before public completion claims.

Status: GitHub change and structural checks confirmed; device validation and independent academic sign-off pending.
