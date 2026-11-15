# Qualitative Curriculum Audit — Phase 4: Questions, Scaffolding, and Evidence Limits

**Audited branch:** `coursework/batch8-independent-incident-response`
**Scope:** Primary `curriculum.json` (all 26 courses and 198 lessons); `exams.json` (24 examinations).
**Method:** Actual full JSON blobs fetched from GitHub. Structural and statistical checks are reproducible; editorial assessment and live device execution are not yet complete.

## Findings and corrections

### 1. Core quiz answer-location bias — corrected in development branch

At the start of this phase, **185 of 198** correct options were at index 0, **13 at index 1**, and **0 at index 2**. This severe positional bias enabled guessing without mastering the subject.

The developer-branch correction rotates existing answer choices into predetermined balanced positions based on course/lesson position while updating the stored correct-answer index. The correct answer **text** remains unchanged, the incorrect choices remain the same, and every question prompt, explanation, lesson title, course order and positional progress identifier remains unchanged. **132 quiz option arrays** were reordered. The resulting index distribution was reverified directly from the GitHub blob: **66, 65 and 67**.

This is a content change to existing multiple-choice presentation, not a migration of completed lesson progress. It does require real browser regression checks to ensure the student always receives appropriate grading and explanations. The audit found zero duplicate question prompts and zero duplicate answer-choice strings within a single primary-lesson question.

### 2. Core instruction template repetition — editorial blocker

Direct inspection of lesson bodies found two large reused instructional scaffolds:
- One template beginning **“GUIDED ANALYSIS: First identify the actors…”** occurs in 84 lesson bodies.
- Another beginning **“PURPOSE AND RELEVANCE: Explain how this topic…”** occurs in 80 lesson bodies.
- **164 of the 198 core lessons** contain at least one of these two reused scaffolds.

The repetition does not make every lesson inaccurate; however, it means lesson length and apparent breadth can overstate topic-specific teaching. The first priority is to inspect lessons for exact mechanisms, domain-appropriate worked solutions, realistic troubleshooting outputs, and original independent practice. Removing repeated text without adequate replacement would make the curriculum worse. This phase **did not** remove or replace the repeated scaffold automatically.

### 3. Examination inventory and alignment — partial verification

The existing `exams.json` contains **24 exam objects and 175 question records**. Every one of the 26 core course titles appears in at least one exam's declared `courses` linkage. This is **nominal course coverage only**; a linked exam may still have too few questions to evaluate the course comprehensively.

Exam-bank correct-answer indices are **95 at index 0, 45 at index 1, 35 at index 2**. The exam bank is less concentrated than the primary lesson quizzes but still needs content quality, distractor and competency alignment review. Two exams cover supplemental computer-building/home-lab course titles beyond the 26-course primary catalog.

### 4. Safety and practical skill — not yet signed off

Existing real-device workbooks, offline cases, and localhost exercises remain distinct from in-app primary lesson quizzes. The lab sources are educational but not a blinded or supervised test of independent hardware, Windows/Linux, network or red-team skills.

## Changes committed in this phase

- Updated `curriculum.json` with balanced answer choices across all 198 core lessons and **preserved correct-answer text**.
- Extended `tests/test_core_curriculum_depth_integration.py` with answer-distribution, prompt uniqueness and unique-option checks.
- Did **not** edit the 24 exam objects, existing grades, progression indices, Firebase records or production site.

## Remaining qualitative completion gates

1. **164 scaffold-bearing lessons:** human review and targeted replacement with distinct worked solutions, verified domain-specific details, and nontrivial independent assignments. Audit accuracy before deleting boilerplate.
2. **175 exam questions:** map each to a specific course objective, analyze distractor plausibility, remediate superficial questions, and verify explanations.
3. **Real practical assessments:** trace individual course outcomes to observed Windows/Linux and hardware evidence and a reliable independent evaluation rubric. Never equate a fictional written exercise with physical device competence.
4. **Browser verification:** ensure all answers still grade correctly and explanations are shown, with completed progress preserved on test profiles across iPhone, desktop and PWA.
5. **CI run results:** verify actual Python regression outcomes, not just Vercel preview build status.
6. **Independent technical/editorial sign-off:** a separate milestone that cannot be inferred from internally authored tests or word counts.

## Suggested next targeted repair

Prioritize the **Security Assessment and Reporting Workshop, Networking and Internet Fundamentals, and Ethical Hacking Hardware Foundations** for a detailed lesson-by-lesson originality pass, because their content must transfer beyond quick recall into authentic technical and professional performance. Report exact lesson fixes and real grading/test results rather than adding another generic batch.
