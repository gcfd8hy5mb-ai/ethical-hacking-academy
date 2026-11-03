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
