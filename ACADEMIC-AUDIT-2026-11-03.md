# Ethical Hacking Academy — Curriculum Inventory and Learning-Journey Audit
**Audit date:** 2026-11-03  
**Scope:** GitHub repository, original `curriculum.json` blob (fully retrieved), hardware track, all three lesson supplements, learning pathway, examination catalog, and stateful practical checkpoint.

## Verified full inventory
The original `curriculum.json` (version 36) was recovered by its Git blob SHA after the ordinary repository file reader returned an empty body. This resolves the earlier incomplete-inventory limitation.

| Authored source | Course count | Lessons |
| --- | ---: | ---: |
| Original curriculum | 26 | 198 |
| PC building and home lab track | 3 added courses | 30 |
| Foundation supplements | Appended to existing courses | 18 |
| Systems and reporting supplement | Appended to existing courses | 12 |
| Applied security supplement | Appended to existing courses | 15 |
| **Combined actual loaded lessons** | **29** | **273** |

The app's loader adds new hardware courses and appends 45 supplemental lessons by exact title, leaving existing course and lesson indexes in place. The audit found no exact duplicate lessons within the same course among these authored inputs. All 273 stored lesson records have six expected fields, valid 3-or-more-answer options, and valid correct-answer indexes. These structural checks do **not** constitute a legal, academic or technical accuracy certification.

## Eight-level plan, after remapping Hardware Foundations
| Level | Planned study hours | Courses | Loaded lessons |
| --- | ---: | ---: | ---: |
| 1: Computer & IT Fundamentals | 35 | 4 | 32 |
| 2: PC Building, Hardware & Repair | 45 | 4 | 52 |
| 3: System & Network Administration | 75 | 5 | 59 |
| 4: Cybersecurity Foundations | 55 | 7 | 48 |
| 5: Ethical Hacking Fundamentals | 75 | 5 | 37 |
| 6: Home Labs, Servers & Virtualization | 45 | 2 | 23 |
| 7: Advanced Red Team Operations | 75 | 2 | 22 |
| 8: Capstone & Mastery | 35 | 0 standalone lesson courses | 0 (practice, portfolio and qualifications) |
| **Total** | **440** | **29** | **273** |

The exact-original 20-lesson course `Ethical Hacking Hardware Foundations` was previously unmatched and silently assigned to Level 4 by the app fallback logic. It is now explicitly positioned first in Level 2. This corrects the learning sequence **without changing source course indices or recorded lesson progress IDs**.

## Assessment coverage
- Existing exam catalog initially held 22 exams (157 questions). Two exams (18 new questions total) were appended to the end of `exams.json`: `PC Build, Repair and Diagnostic Decisions Examination` and `Workstation, Virtualization and Home Lab Readiness Examination`.
- The updated catalog contains **24 authored examinations with 175 questions** and an 80% pass threshold. Exam indexes 0–21 are unchanged, preserving stored historical best-score keys.
- Every loaded course now appears in at least one `exams.json` exam's course mapping.
- Four Level 3–7 system/reporting supplemental courses, lab simulations and final qualifying exercises remain separate from ordinary course exams.
- Eight synthetic troubleshooting/practical checkpoint scenarios are shared across levels. Level 8 reuses all eight as cumulative review; this is **not eight brand-new capstone scenarios**.
- Readiness after the preceding audit recognizes Level 8's actual Part I and Part II simulated qualification exams. It does not represent externally certified competence.

## Study-time realism and remaining work
All 273 lessons contain approximately **140,629 words of main lesson reading** in the loaded records, with a median reading length around **484 words** (the briefest around 116 words). This excludes lab instructions kept in separate HTML files and assessment explanations. **The 440 hours remain a planning allocation, not objectively measured required study time.** Reading alone would not plausibly account for those hours; the program needs sufficiently substantive lab, practice, investigation, project, assessment and remediation workloads. Some lessons, particularly brief supplemental and PC hardware entries, need depth or practical-work validation without merely expanding reading volume.

Highest-priority next steps:
1. Record estimated guided reading, active lab, written work, assessment and remediation time per course and level using reproducible criteria; do not manufacture study-hour equivalency.
2. Detect meaningful conceptual overlaps across 273 lessons, beyond exact title duplicates; prefer linking/reviewing existing lessons instead of deleting lesson IDs or adding repetitive study hours.
3. Validate course-to-exam alignment and scenario diversity in live browser sessions; question-count and schema audits do not prove examination quality.
4. Run actual iPhone Safari and Home Screen tests plus desktop tests for navigation, completion, exam result retention, lab state, and Back buttons.
5. Verify Firebase cross-device save for lesson progress; standalone checkpoint state is still browser-local and is **not proven** cloud-synced.
6. Assess proficiency in isolated, authorized real systems and obtain independent technical review of reports and exercises before claiming any professional equivalence.

## Safety and acceptance constraints
No original curriculum or lesson index was removed, moved, or overwritten. No existing Firebase progress documents or scores were reset. All practical test environments must remain owned or explicitly authorized and isolated. These changes do not grant academic accreditation, professional certification, legal permission to test unknown targets or a guarantee of operational Red Team proficiency.

## Changes verified in this audit
- `learning-pathway.json`: Explicitly maps original Hardware Foundations to Level 2.
- `exams.json`: Appends two previously missing assessment mappings, retaining earlier exam order.
- Earlier audit fixes: valid lesson-count display, final qualification readiness, and accurate explanation of Firebase limitations.

## Practical-depth expansion and proposed hour allocation (2026-11-03 continuation)
The eight-level 440-hour **planning target** is now broken down into **73 guided-instruction hours, 271 practical-work hours, 64 exam/reporting hours and 32 remediation hours**. The allocations are estimates to guide curriculum editing, not measurements of authored content or guarantees of completion time. They are inclusive of the existing study budget; no additional 440 hours were created.

An integrated **Enterprise Case Portfolio** was authored and linked to Levels 5–8 and the Practice Lab. It includes three cross-system, fictional and authorized scenarios (identity change with web outage; cloud IAM/network drift with backup recovery; professional assessment closure), five evidence interpretation decisions per scenario (15 questions total), and free-form executive/technical reports. The 80% threshold is attainable with four correct answers out of five; these are **separate case decision checks**, not additions to the 24 normal examinations or the 273 lesson count. Proposed 4–7-hour workload per case includes analysis and report work and must be observed/verified before inclusion in any externally evaluated study-hour total. The portfolio uses a new browser-local record key; its results do not yet cloud-sync or substitute for human assessment.

The primary remaining risk remains **validating depth**, particularly whether 271 planned lab hours correspond to substantive guided and independent technical exercises. Before academic sign-off, run live iPhone and desktop acceptance tests, real isolated-lab exercises, graded report reviews, and cross-device cloud-save verification.

## Practical field guide expansion (November 3, 2026)
Added `real-system-lab-field-guide.html` with **three explicitly scoped exercise guides**: Windows workstation networking and service diagnosis (3 hours planned), Linux service/log/permission diagnostics (3 hours planned), and isolated dual-VM network segmentation (4 hours planned). The 16 command walkthroughs include what each command does, sample/expected outcomes, interpretation, safety boundaries, verification and rollback; students can save and export local notes and self-evaluation checklists. Linked in Levels 3, 6 and 7 and the main Practice Lab. These **10 planned hours are already within the 440-hour study budget**, not an increase. No real environment or actual human competence has been verified. Notebook records use the distinct browser-local `ethical-hacking-real-lab-fieldbook-v1` key and are not confirmed to sync with Firebase. Live iPhone and desktop tests and measured time-on-task remain outstanding.

## Independent diagnostic challenge (2026-11-03 continuation)
Created `independent-diagnostic-challenge.html` with three enterprise case families and two alternative evidence scenarios each (six total). Each variant requires three independent choices: supported cause, safe authorized response, and post-change verification. Corrective decisions are scored after evidence review, with optional locally saved and exported professional reports. These are fictional decision exercises; they execute no operating-system commands and do not replace real-machine competence tests or human grading. Linked from the Practice Lab and Levels 5, 7 and 8. No existing course, exam index or progress storage key changed, and no extra planned hours were added beyond 440. A student-device acceptance test remains outstanding.

## Hands-on competency evidence review (2026-11-03 continuation)
Added `hands-on-competency-review.html` with four competency exercises: Windows configuration and service reasoning, Linux identity/log/listener diagnosis, isolated virtual-network boundary verification, and Level 8 professional report defense. Across these, 21 explicit command/analysis steps explain purpose, evidence interpretation and limits; each has safe authorized scope, validation, cleanup/rollback guidance, an evidence notebook and five self-review criteria. Linked to Levels 3, 6, 7 and 8 plus the main Practice Lab. Reports remain in separate device-local storage (`ethical-hacking-hands-on-competency-review-v1`) and can be exported as text. No live machine is read or controlled and no task is automatically certified; a human must assess accuracy, authentic machine evidence and independence. No new normal lessons or exam-score keys were added, and the 440-hour program budget is unchanged. Code-level syntax and navigation checks passed; live iPhone and Windows/Linux acceptance tests have not yet been performed.

## Evidence-review process (2026-11-03 continuation)
Added `competency-evidence-review.html`, a browser-local assessor workflow reading the four existing hands-on notebook records (Windows, Linux, isolation and professional report). It surfaces submitted observations, reasoning, correction/retest evidence, and checklist status. A named reviewer or student may record five rubric checks, an outcome, rationale and a review timestamp; the page explicitly warns that reviewer identity and machine evidence are not independently authenticated. Each saved review captures a lightweight content fingerprint and warns if a notebook changes afterward. A report package can be exported. A separate key, `ethical-hacking-competency-assessor-records-v1`, holds the assessor notes; **no existing student progress, exam record or Firebase document is overwritten**. Synthetic mastery, enterprise-case and diagnostic outcomes are shown as contextual counts only. Linked from Levels 3, 6, 7 and 8. Main Practice Lab link still pending due to repository write rejection. JavaScript syntax checks pass, but live iPhone acceptance and actual independent evaluation are outstanding. The existing 440-hour planning budget is unchanged.

## Portable practical-evidence transfer (2026-11-03 continuation)
The inspected `firebase-cloud-v3.js` collector serializes all `localStorage` records whose names start with `ethical-hacking-`, including recent practice portfolios and review keys, into an opt-in Firebase coursework snapshot. This means the keys are *eligible* for inclusion in the broad snapshot, but actual cross-device preservation requires a connected account, matching revisions and live verification; the conflict safeguard pauses rather than auto-merging different copies.

Added `practice-evidence-transfer.html` with an export/import bundle containing six explicitly whitelisted practice and competency record collections. Normal lesson completion, exam results and cloud authentication keys are never included. JSON imports are validated, capped at 2 MB, previewed by collection and case, and **add missing case records by default**. Conflicting existing case records are preserved unless the user explicitly checks their replacement option. Import requires acknowledgement of an independently downloaded backup, and import changes are limited to these whitelisted local keys; there is no direct Firestore write. The page is linked from the main Practice Lab and Levels 3, 6, 7 and 8. The relevant scripts passed syntax checks; live cross-device behavior, file-picker compatibility and Firebase reconciliation still need hands-on acceptance tests. The 29-course/273-lesson catalog, 24 normal exams and 440-hour planning allocation are unchanged.

## Firebase device-restore acceptance tests (2026-11-03 continuation)
The existing `firebase-cloud-v3.js` was inspected end-to-end. It already supports opt-in Firestore snapshots, mismatch comparison, manual device-to-cloud replacement, revision-guarded transactions, and a downloaded two-version backup. Its original compare flow lacked an explicit Firebase-to-device recovery path: a new device with different or empty records could not select an existing cloud copy.

A new **Restore Firebase copy on this device** action was added only when a cloud/device difference exists. It requires the user to request both-device/cloud backups and twice confirm the specific local replacement. Before touching records it rechecks the active authenticated account, local snapshot stability, cloud record revision, and cloud raw contents. It then restores the cloud's matching `ethical-hacking-` storage namespace, removes local-only keys in that namespace (the downloaded backup holds the prior device copy), records the cloud-link revision, and reloads the coursework to refresh in-memory lesson progress. Any storage failure attempts to roll back changed local keys. The original device-to-cloud overwrite action now also requires the download step. Firestore is not written by the device restore.

**Isolated script-based test results (not a live Firebase test):**
- Browser module syntax: passed after import declarations were excluded for parsing.
- Restore blocked before backup download: passed.
- Cloud-to-device record replacement and requested page reload after both confirmations: passed.
- Restore transaction writes to Firebase: none.
- Cloud revision changed after comparison: abort without changing progress, passed.
- Local practice record changed after comparison: abort without replacing progress, passed.

The test harness used fake browser storage, Firebase API responses and a simulated account. **Outstanding acceptance:** real iPhone Safari and saved Home Screen flow, signed-in same-account desktop retrieval, download verification in iOS Files, real Firestore race and permission validation, account-switch tests, large-document quota/storage failures, and checking imported practice records on the second device. Do not infer cross-device acceptance or full practical-evidence sync from these isolated tests.

`index.html` now cache-busts the changed Firebase module with `restore-safe-v6-20261103`. Student lesson/exam IDs, course content, and 440-hour planning workload were not altered.

## Applied-security lesson depth expansion (2026-11-03 continuation)
Academic-review continuation focused on the **15 existing lessons** in `coursework-applied-security-v1.json`. Their original readings averaged approximately 150–170 words each and required more explicit method/interpretation examples. All fifteen lessons were enhanced in-place with approximately **1,565 additional words** across five courses: enterprise IAM (Level 3), security monitoring (Level 4), web application security (Level 5), cloud infrastructure (Level 6) and professional security analysis (Level 7).

Additions include fictional policy and event examples, timestamp normalization, safe read-only command examples on authorized systems, authorization-positive/negative testing, backup RTO/RPO reasoning, objective retest criteria and graded written evidence artifacts. The changes deepen existing explanations and do not add new lesson IDs, course titles, assessments, or planned hours. Follow-up structural validation confirmed each of the 15 records retains the expected six fields, answer options and a valid correct-answer index; all five affected courses retain normal examination mappings. The expanded lesson readings now range approximately 249–308 words. This does **not** certify academic correctness; subject-matter verification and review of other short lessons remain open.

**Next depth-review targets:** the 12 `coursework-systems-redteam-v1.json` lessons (roughly 147–198 words each before expansion), then the 18 foundation supplement lessons and an assessment-question reasoning audit. Do not change original course/lesson positions because of saved progress.

## Systems/networking lesson-depth expansion (2026-11-03 continuation)
Continued the short-lesson audit on the 12 existing lessons in `coursework-systems-redteam-v1.json` (Windows Administration and Security; Linux System Administration Lab Theory; Networking Practice and Troubleshooting; Security Assessment and Reporting Workshop). Added approximately **1,019 words** of practical diagnostic interpretation and safety/verification instruction to these lessons, without changing titles, quiz answers, lesson positions or saved-progress IDs.

New work covers read-only PowerShell service and OS inspection, Windows timeline reconstruction and internal DNS discovery, Linux listeners, permission and inode/disk diagnostics, isolated-VM subnet reasoning, and professional scoped assessment reporting. Practical instructions explicitly distinguish sample evidence from actual device observations, require permission, avoid production-system modification, and specify validation and rollback.

**Combined academic-development batch:** 15 applied-security lessons plus 12 systems/reporting lessons = **27 existing lessons enhanced**, approximately **2,584 words of targeted additions**. Subsequent structural validation verified all 27 six-field lesson records, answer-index validity, course-to-level placement and existing examination mappings. Median reading length across these 27 is approximately 263 words; full lesson-hour equivalence is still not demonstrated. The catalog remains 29 courses and 273 lessons with 24 conventional exams and a 440-hour *planning* target. Neither actual lab completion nor independent scholarly correctness has been certified.

Next review candidates are the shorter foundation supplements, incomplete experiential depth within the 440-hour budget, and exam-level content alignment.

## Foundational depth and examination-bias audit (2026-11-03 continuation)
Expanded all **18 existing foundation supplements** in `coursework-foundations-expansion-v1.json`, adding approximately **2,001 words** of targeted practical instructions. The six courses involved are Getting Comfortable With Computers; PC Building & Computer Hardware; PC Assembly, Repair & Troubleshooting; Beginner Linux and Terminal Skills; Networking and Internet Fundamentals; Cybersecurity Foundations. The additions include read-only/safe commands, output interpretations, diagnostic alternatives, hardware electrical precautions, authorization/privacy limits, measurable submissions and rollback. No lessons or course positions were changed. A post-update structural check passed all 18 six-field lesson records and quiz answer indexes; each course remains mapped to both its level and at least one examination. Revised lesson readings ranged from approximately 217 to 280 words. All 18 still need independent technical-editor review before sign-off.

**Combined depth edits to date:** 15 applied-security + 12 systems/networking + 18 foundational = **45 existing lessons improved in place**, with approximately **4,585 added words**. The total remains 29 authored courses, 273 lessons, 24 conventional examinations, and a 440-hour planning allocation (not externally validated study time).

**Exam-bank audit:** All 24 exams and 175 questions passed basic option-count, answer-index and nonempty-explanation structural checks, with no exact repeated question stems detected. Critically, the earliest eight examinations (50 questions) had correct answer index 0 for *every* question. The browser exam interface `exams-ui.js` now shuffles displayed choices on each new attempt while retaining original question/answer indexes for grading, source data, saved best-score history, and review explanations. Grading keys are unchanged; a prior saved score is still just a historical exam outcome, not independently verified mastery. `app.js` import and `index.html` cache versions were updated to load the UI fix. Syntax validation and 200 isolated shuffle-permutation checks passed (165 of 200 permutations were not the original 0/1/2 order). No live user-device assessment has been executed.

**Remaining exam-quality review:** Evaluate distractor plausibility, discrimination between conceptual knowledge and practical reasoning, answer length/wording clues, topic-weight balance, and human subject-matter assessment. Display shuffling corrects the answer-position exploit, but cannot alone prove exam rigor.

## Examination distractor quality audit and advanced diagnostic (2026-11-03 continuation)
Review expanded beyond basic exam schema and the earlier answer-position shuffle. The baseline **24 exams / 175 questions** have a highly uneven original answer-index distribution (**95 position 0; 45 position 1; 35 position 2**), though the normal exam UI shuffles displayed options by attempt. The first eight examinations, totaling 50 questions, previously had every keyed correct answer at index 0. Heuristic content checks flagged **15 questions with obviously unrelated distractor wording** (such as wallpaper/toner in technical-security questions), approximately **52 potentially revealing longest-correct-answer patterns**, and **53 explanations shorter than 10 words**. These are heuristic editorial triage counts, not independent psychometric analysis or final judgments on all questions.

To avoid invalidating existing historical exam scores and their question versions, no existing exam prompt, answer, score key, or exam index was edited. Added an **optional** four-track `advanced-reasoning-diagnostic.json` and `advanced-reasoning-diagnostic.html` with **16 original scenario questions**, evidence-based competing alternatives, substantial feedback after each submission, a new separate local best-score key, and per-attempt display-order shuffling. Tracks cover Systems/Network Diagnosis (Level 3), Identity and Application Authorization (Level 5), Cloud/Recovery (Level 6), and Professional Engagement/Retest (Level 8). The optional result does not affect mastery or ordinary examination grades. The new diagnostic is linked in the main Practice Lab and Levels 3, 5, 6 and 8; changed JavaScript and structured question schemas passed static checks, and the course's 440-hour planning allocation is unchanged.

Remaining work: a manual question-by-question editorial rewrite of weak existing distractors with assessment versioning or an explicit history-retention policy, accuracy and discrimination evaluation by qualified reviewers, questions calibrated for real command/result interpretation, and actual student-device acceptance checks. The new diagnostic's four-item tracks provide practice and formative assessment, not a statistically reliable or externally accredited competency measurement.

## iPhone coursework startup reliability correction (2026-11-03)
A supplied short iPhone screen recording showed the student login form and then a light screen displaying **Loading coursework...** after sign-in. This confirms a coursework startup problem in the recording, not a failure to display the authentication form. Static inspection of `app.js` and seven imported UI modules found no JavaScript syntax errors; direct live GitHub Pages behavior could not be verified from the available web tool.

The Academy had fetched its main catalog and numerous supplementary JSON resources in a largely sequential startup path, postponing the first render until all supported resources finished. Updated `app.js` to launch **11 optional course/exam/support requests concurrently**, cache their request promises within the page and bound pending requests with a 15-second abort; the main course catalog still must be successfully fetched. A loading-status message is shown while fetching the main catalog. Updated `index.html` with a 25-second conditional startup fallback offering a reload button if a signed-in session still displays the default loading placeholder. Updated the `app.js` cache version. Scripts passed parsing/static checks. No lesson IDs, stored progress or Firebase records were modified. No service worker file was found under `sw.js` or `service-worker.js`, though Safari/PWA HTTP caching still warrants device validation.

**Outstanding:** confirm the GitHub Pages deployment is serving the new files, test iPhone sign-in and full curriculum render, inspect real network/console errors if the fallback appears, and confirm that the full 29-course catalog loads with all supplements. A six-second recording alone cannot establish whether a slow network request would have completed later. Cross-device cloud tests remain deferred by user request.

## Core-first startup recovery after repeat iPhone failure
User reported iPhone still stuck loading after earlier timeouts and concurrent downloads. Root-cause inspection identified a **blocking static import chain**: `app.js` had seven top-level imports for optional lab, diagnostics, simulator, written assignments and examination UI modules. If any imported dependency failed to download/initialize, the main module would not run at all, preventing even the main Academy catalog from rendering. An additional risk was 11 optional JSON requests competing for network bandwidth before the 1 MB primary catalog was fully parsed.

Corrective commits removed all seven startup-blocking imports and replaced them with **lazy imports triggered only when the relevant practice or exam view is opened**, with per-section errors. The main catalog is now downloaded and parsed **before** other curriculum resource requests begin. Optional supplement resources are requested concurrently afterward with bounded timeouts. The app displays a concrete retry/action screen if the primary catalog fails rather than remaining indefinitely on a loading placeholder. `index.html` app script cache version updated to `core-first-lazy-modules-v33-20261103`.

Verification used an isolated evaluation of the actual repository `app.js`, primary `curriculum.json` downloaded through the GitHub blob API, and six relevant support JSON files. **Full startup passed and produced the home screen with 29 courses and 273 lessons, no errors.** A separate run with optional files unavailable still rendered the core home screen (26 original courses) rather than failing startup. New script syntax checks passed. No saved student, examination or Firebase data were cleared or modified. Real iPhone Safari, Home Screen app and GitHub Pages deployment remain to be checked by the user; no live browser/production Firebase test was possible.


## Repeated iPhone startup failure: auth refresh and independent diagnostics
After the user reported a persistent loading failure despite core-first and optional-module isolation, we inspected `auth.js` and found another potential hang: `onAuthStateChanged` awaited an unbounded `user.reload()` call **before removing the `auth-locked` class**, which hides the Academy content. This could leave the UI hidden if Firebase account refresh never resolves on iPhone. The account refresh is now bounded to eight seconds; failure does not treat an unverified account as verified. If the Firebase SDK already reports `emailVerified: true`, the app can proceed without indefinitely waiting for the network refresh. The auth module was cache-busted in `index.html`.

Added a standalone, no-sign-in `startup-diagnostic.html` with timed read-only checks for public Academy HTML, application JavaScript, core curriculum JSON, three supporting course/exam resources and the public Firebase application/authentication libraries. The report shows file-specific errors and load timing without collecting student grades or credentials, and is linked from the Academy's initial page. Static JS checks passed. These changes did not modify saved lessons, examination grades or Firebase records.

**Unknown:** the exact root cause on the affected iPhone. Public GitHub Pages resources were not accessible to the available external web fetch at review time; this is not proof that the user's browser cannot access them. Have the user run the new diagnostic and share the result screen. Do not claim the site is fixed without an iPhone acceptance test.


## Live iPhone runtime startup diagnostic instrumentation
User's actual iPhone Safari diagnostic output verified all eight public resource fetches: main HTML, `app.js`, core `curriculum.json` (1,068,778 characters), PC building, foundation supplement, 24-examination JSON, Firebase app library, and Firebase Auth library. Each completed successfully in ~24–184 ms. This is strong evidence against a basic public resource fetch failure on that device, but it does not establish that module evaluation, authentication, or rendering completed.

To isolate the remaining failure, `startup-runtime-debug.js` was created as an **opt-in, read-only** overlay activated with `?debug=1`. It records staged initialization markers and top-level `error` and `unhandledrejection` events without reading student progress, credentials, or examination answers. Stages were inserted into `auth.js` (form displayed, auth state callback, refresh result, unlocked view) and `app.js` (main script start, curriculum retrieval/parsing, completed render, startup failure). The diagnostic script loads before Firebase and Academy modules in `index.html`, with cache-version updates. JavaScript syntax checks passed for all changed scripts. Live user screenshot still needed; **do not claim fixed until tested**. Cloud sync and student progress are unchanged.


## Definitive Safari startup syntax error and repair
A live screenshot of the Academy's opt-in iPhone startup overlay reported `SyntaxError: Cannot declare a function that shadows a let/const/class/function variable 'masteryPanel'`. The diagnostic simultaneously showed Firebase authentication returning `verified=true` and unlocking the course view, while the main app remained at the loading placeholder. This establishes a **fatal Safari JavaScript parse error before the Academy app initialized**; previous resource downloads were successful and were not the root cause.

Inspected `app.js`: it declared `function masteryPanel(c,i)` for a single course and later `function masteryPanel(level)` for level readiness. Renamed the first to `courseMasteryPanel(c,i)` and its sole course-page call to `courseMasteryPanel(c,courseIndex)`; the level function and its calls were preserved. Confirmed exactly one definition for each and checked all top-level `function` names for duplicates (none), main script syntax, and the existing eight-level pathway. Updated `index.html` cache reference to `app.js?v=mastery-panel-safari-fix-v35-20261103`. No curriculum data, Firebase records, exam history or lesson completion keys were changed.

**Next acceptance step:** user should reopen the Academy with `?debug=1&v=35` on iPhone and verify the overlay progresses through primary curriculum parsed, coursework ready and home rendered; only then consider the issue resolved. The external web fetch could not independently access the published GitHub Pages URL, so the deployed iPhone test is still outstanding.


## Versioned examination quality revisions — eight foundational exams
Resumed curriculum audit after actual iPhone Safari and Home Screen launch were confirmed working. Preserved legacy `exams.json` (version 7, 24 exams, 175 questions), existing `ethical-hacking-exam-results-v1` local records, original correct-answer meanings, and their course-to-exam mappings.

Created `exams-revised-v2.json`, a **versioned alternative bank covering the first eight foundational examinations (52 questions)**. Editorial revisions replaced implausible or misleading incorrect options and added context-rich answer feedback to **36** questions, including backup independence, filename interpretation, DNS and service diagnosis, authorized assessment, identity control, web authorization, hardware safety, and defensible reporting. The other 16 questions retain their options and receive additional explanation text. The source question stems and correct answer text were preserved across all 52, with no shifted original IDs.

The Academy `exams-ui.js` now offers revised V2 exams first, marked **UPDATED**, and the 24 original exams afterward marked **LEGACY**. New revised scores are stored **only** at `ethical-hacking-exam-results-revised-v2`, while old exam scores and mastery calculations continue using `ethical-hacking-exam-results-v1`. Revisions do **not** silently confer old mastery credit or rewrite historical grade meaning. Choice order remains shuffled per attempt; feedback is shown after grading. Updated `app.js` lazy import and `index.html` cache version for Safari.

Verification: the revised bank has 8 exams and 52 questions; all revised question schema/answer indices and explanations passed, all 52 original stems and correct-answer strings match the legacy bank, and the first 36 question changes match targeted distractor edits. The original 24 exams and 175 questions were unchanged. UI and main script syntax checks passed; no duplicate top-level function names remain. **Live revised-exam iPhone interaction not yet tested.** The 440-hour overall study allocation remains a plan, not an accredited measurement.


## Revised V3 foundational and intermediate examination editorial audit
Continued the academic quality review after Safari and Home Screen app loading were confirmed functional. Preserved the untouched legacy `exams.json` bank (24 exams / 175 questions, version 7), existing V2 revision bank (8 exams / 52 questions), historical mastery calculation rules and all original progress records.

Created `exams-revised-v3.json` to cover legacy examinations **8–16 inclusive** (nine exams / **45 questions**): computer and OS fundamentals, networking, security architecture/threat modeling, service operations, defensive cryptography, security monitoring, authorized assessment, network reasoning, and introductory Python/defensive automation. All 45 questions received question-specific explanations addressing *why* the keyed choice follows and *why* alternatives are less defensible; **28 questions** received more plausible incorrect alternatives (e.g., differentiating routing from DNS and HTTP outcomes, confidential key handling, approved scope, monitoring metrics, rollback, and evidence limits). Each new explanation is at least 21 words. Original question stems and keyed correct-answer text remain identical. These are educational editorial revisions, not independent subject-matter or psychometric certification.

Modified `exams-ui.js` to display optional **UPDATED V2** and **UPDATED V3** choices before all 24 **LEGACY** exams. Revised V3 best scores use their own new storage key `ethical-hacking-exam-results-revised-v3`; V2 retains `ethical-hacking-exam-results-revised-v2`, while original mastery and grade data retain `ethical-hacking-exam-results-v1`. Correct answer grading is still based on source choice indexes despite per-attempt shuffling. App script cache versions changed for iPhone.

Static checks passed: V3 contains exactly 9 mapped exams / 45 questions, 28 question-option revisions, zero stem/correct-answer/key mismatches, valid question arrays, valid JS module and main app syntax, all three distinct score-key references, no duplicate top-level app functions. No iPhone V3 exam-taking test performed yet. **Across V2 and V3:** 17 distinct original exams have revision alternatives covering **97 questions**. The remaining **seven legacy exams, 78 questions** (exam indexes 17–23, mainly comprehensive finals and hardware readiness) require a similar manual quality review. The overall course catalog and 440-hour planning budget remain unchanged.


## Revised V4 comprehensive, hardware and lab examination audit
Completed the last batch of versioned **editorial** exam revisions in `exams-revised-v4.json`: the remaining **seven legacy exams, 78 questions** (original indexes 17–23), including Systems and Networking Comprehensive Final; Defensive Security and Incident Response Final; Authorized Assessment and Web Cloud Final; Evidence Interpretation and Decision-Making Final; Cloud Identity and Software Assurance Final; PC Build, Repair and Diagnostic Decisions; and Workstation, Virtualization and Home Lab Readiness. Every question received a topic-specific, explanatory rationale (minimum 19 words) and 28 questions had distractors replaced with more plausible technical alternatives.

The revision preserves all original question stems and correct-answer texts. Static checks found zero question-index, correct-answer, or schema mismatches. The original `exams.json` was not edited; all **24 legacy exams and 175 questions** remain available. Revised exam banks now cover all 24 original exams: V2 (8 exams / 52 questions), V3 (9 / 45), V4 (7 / 78). The Academy's examination UI lists **UPDATED V2**, **UPDATED V3**, **UPDATED V4** followed by **LEGACY**, with randomized answer presentation and a separate best-score local key for each revised bank. Legacy course mastery continues to use only `ethical-hacking-exam-results-v1`; V2, V3 and V4 grades never silently change old results. Main Academy import and iPhone cache versions were updated.

Static verification: V4 has seven exams and 78 questions, 28 option revisions; all keyed answer texts and stems match source; V2/V3/V4 together cover 24 of 24 original exams. Examination UI and main app JavaScript syntax checks passed, and no duplicate top-level app function declarations were found. **Caveats:** these are edited-formative alternatives, not independent validated equivalents of the original exam's difficulty; live iPhone exam-taking, distractor discrimination, instructional alignment and independent expert subject-matter review remain outstanding. No changes to cloud sync, 29 courses, 273 lessons, or the 440-hour planning budget.


## Evidence-based practical skills standards across eight levels
After completing the 24-exam editorial revision coverage, reviewed the eight-level `learning-pathway.json`, three supplemental coursework packs (45 appended lessons total), and existing practical guides. Found clear planned hour allocations and practical lab entry points, but **planned workload is not the same as verified independent skill**. Level 8 intentionally has no traditional course mapping and is assessed through capstone resources; this should not be interpreted as missing lessons alone. A full stopwatch-based study-time validation and independent academic/program review remain outstanding.

Created `practical-competency-standards-v1.json` covering all eight planned levels and **24 observable performance tasks** (three each), with task steps, expected evidence packages, safe practice environments, explicit critical failure rules, and cautions separating Academy simulations from verified real-machine work. Introduced a consistent 100-point evidence rubric: technical accuracy 25, observed evidence 25, interpretation 20, authorization/safety 20, verification/rollback 10. A score of 80 is only a **threshold for possible instructor review**, not an automated qualification. Safety violations always override scores. Evidence must avoid passwords, private records, unrelated network access and unapproved real-world testing.

Built mobile-friendly `practical-competency-standards.html` that loads the above JSON, enables selection among the eight levels, shows all required tasks and safety gates, provides a local non-persistent score calculation, and supports copying a blank practical evidence template. The guide does **not** change lesson completion, examination grades, mastery status or cloud data. Integrated direct links from the Academy's level screens and Practice Lab; refreshed the versioned `index.html` main-script reference for the iPhone.

Verification: standards JSON parses, 8 levels × 3 tasks = 24 tasks, planned hour references sum to the existing **440 hours**, rubric adds to 100, safety gates present; guide JS and main app JS parsed with no syntax errors and no duplicate top-level function names. No iPhone guided-assessment acceptance test or independent reviewer assessment has yet been performed. Next audit: measure authored workload per lesson/lab against targets; test every 8-level lab link and device behavior; review real-hardware evidence versus synthetic completions.


## Authored instructional workload and advanced lab gap audit
Audited all 29 assembled course identities and **273 lessons** against the eight-level pathway, using original `curriculum.json` (26 courses / 198 lessons), PC Building track (three courses / 30 lessons), and three additional lesson packs (18 + 12 + 15 lessons). Counted approximately **145,364 words of authored lesson instructional text** across the combined catalog, excluding many external interactive lab pages, assessment explanations and supplementary reading. Word counts are a reproducible **inventory measure, not verified learning hours**. No course names were missing from the pathway and no courses were unassigned.

| Level | Planned hours | Mapped lessons | Authored lesson words | Unique-linked lab entries at audit |
|---|---:|---:|---:|---:|
| 1 — Computer & IT Fundamentals | 35 | 32 | 15,633 | 3 |
| 2 — PC Building, Hardware & Repair | 45 | 52 | 16,847 | 4 |
| 3 — System & Network Administration | 75 | 59 | 39,779 | 10 |
| 4 — Cybersecurity Foundations | 55 | 48 | 26,844 | 3 |
| 5 — Ethical Hacking & Red Team Fundamentals | 75 | 37 | 25,890 | 6 |
| 6 — Home Labs, Servers & Virtualization | 45 | 23 | 10,468 | 10 before new workbook |
| 7 — Advanced Red Team Operations | 75 | 22 | 9,903 | 10 before new workbook |
| 8 — Professional Capstone & Mastery | 35 | 0 direct lessons | 0 direct lesson words | 11 |

Level 8 intentionally uses capstone/qualification resources rather than direct course IDs. Level 6 and 7 have comparatively less conventional written instruction per planned hour; a portion of their time must be genuinely supplied by lab execution and evaluated evidence rather than implied by a target-hour field. The sparsest per-lesson courses observed: Red Team Workstation & Home Lab Engineering (10 lessons, ~1,261 words), PC Assembly, Repair & Troubleshooting (13, ~1,981 words), and PC Building & Computer Hardware (13, ~2,057 words). **This is a depth warning, not proof that lab assignments are absent**; practical pages have their own content and were not included in those word counts.

Checked **24 distinct local HTML lab resources** linked across **57 original pathway lab entries** (excluding the index.html#lab anchor). Every referenced page existed in the GitHub repository and was nonempty. This checks source presence only, **not live browser functionality, simulations, accessibility, correctness, or hardware proficiency**.

Created `guided-lab-expansion-l6-l7-v1.json` with **eight guided cases / 40 explained steps / 700 minutes suggested practice**, emphasizing isolation, service health, snapshot restore, resource sizing, rules of engagement, synthetic timeline interpretation, backend authorization and executive reporting. These are suggested exercise durations, not measured learner activity. Created `guided-advanced-labs.html`, a responsive, read-only guide with step-by-step explanation, evidence checklist, privacy-aware worksheet and critical failure conditions. Linked the guide from the Level 6 and Level 7 learning pathway entries without changing course IDs, progress, examinations or Firebase. Postchange checks passed: guide JavaScript, main app JavaScript, required lab/evidence schema, workbook links in Levels 6–7, 8 labs × 5 steps, unchanged total of 440 planned hours and no storage writes in the workbook.

**Next priorities:** deepen the ~126-word-per-lesson Red Team Workstation/Home Lab Engineering course and the thin PC repair courses; add reproducible output interpretation and measurable lab grading to each. Test the new workbook on iPhone; independently time a representative student's complete lesson + lab + report cycle, and do not claim academic equivalence based only on the 440-hour plan.
