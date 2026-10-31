# Ethical Hacking Academy — Coursework and Assessment Audit

Audit date: 2026-10-31. Source: current GitHub main JSON contents at audit time. This is a data-structure review, **not** an interactive browser/device test or independent security assessment.

## Verified content inventory
- Courses: 26
- Lessons: 198
- Examinations: 20, questions: 133
- Courses assigned at least one examination: 26/26
- Written portfolio assignments: 19
- Interactive diagnostic cases: 9
- Structural lesson/exam mapping problems in this audit: 0

## Changes in this batch
Deepened 34 **existing** lessons in Beginner Linux and Terminal Skills (8), Windows Administration and Security (8), Networking Practice and Troubleshooting (8), and Security Assessment and Reporting Workshop (10). Expanded worked examples, decision steps and verification expectations. Preserved lesson indices and course ordering to avoid invalidating existing device-local completion keys.

## Remaining findings (prioritized)
1. **High:** Many other lessons are short introductory readings, not comprehensive university-level instruction. Expand explanation, worked examples, practice, feedback and citations without counting generic prompts as teaching hours.
2. **High:** Automatic exams remain predominantly recognition-based, and several newly authored course exams have only five questions. Add varied constructed-response and multi-step objective scoring; do not call current exams proctored or externally validated.
3. **High:** Interactive diagnostic labs run only in the browser on **synthetic outputs**, not a real shell or managed virtual machine. Their seven-point score can be improved by revealing all available evidence; it does not prove genuine command skill.
4. **High:** Written reports are self-reviewed and locally stored, with no independent evaluator. Keep these distinct from verified competency and graduation readiness.
5. **Medium:** Existing progress uses browser localStorage keys and index-based IDs; avoid reordering earlier lessons or examinations. Cross-device sync requires a separate authenticated data migration plan.
6. **Medium:** Recent app and mobile layout commits have not been verified by an automated iPhone Safari end-to-end run. Test navigation, grading, persisted scores, reload and small-screen layout on the deployed site.

## Audit checks performed
- Checked each lesson has a valid answer index and answer list.
- Checked each exam question has a valid answer index.
- Checked examination course names map to existing courses.
- Counted all relevant JSON objects and validated the expanded content remains in existing lesson positions.

## Acceptance criteria for subsequent phases
A practical module should present a clear observable scenario, allow meaningful independent choices or command interpretation, assess evidence and root cause separately, supply actionable explanation and retest conditions, and clearly label simulation vs actual device execution.
