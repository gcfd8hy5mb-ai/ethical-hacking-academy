# Ethical Hacking Academy — Multi-stage Coursework Audit
**Date:** 2026-11-07
**Scope:** `multistage-case-investigations-2026.json`, `multistage-case-investigations.html`, `learning-pathway.json`.

## Coverage
- Eight original level headings retained.
- Eight fictional, authorized scenarios: Linux file evidence; POST/memory triage; DNS/routing; SOC identity triage; object-level web authorization; VM isolation; detection rule metrics; multi-cause enterprise incident.
- Four gated stages per scenario (32 total).
- Two decisions per stage (64 total).
- Written reflection of at least 60 words per stage, with no claim of semantic automated grading.

## What was checked programmatically
1. Source JSON loads; exactly 8 cases, 4 stages each, 2 questions each.
2. Options, keyed answer indexes and feedback rationales are present.
3. Grading uses eight binary decisions × 12.5 points for 100 points maximum per case. It does not award points for word count.
4. Curriculum links appear in all eight levels.
5. Existing course arrays remain unchanged (4, 4, 5, 7, 5, 2, 2, 0 courses).
6. Reader script passes JavaScript syntax compilation.

## Academic and technical qualifications
- Source material is **fictional training data**, not an observed real breach.
- Chosen actions are defensible within each provided case's facts, but alternative investigative steps may also be reasonable.
- In particular, a change-ticket overlap does not prove device ownership; DNS health does not prove application recovery; a hypervisor internal switch does not prove perfect containment; exposed API data does not prove a real identity compromise.
- Detection example: baseline TP=9, FP=15, FN=6, TN=70 → precision 37.5%, recall 60%; candidate TP=12, FP=8, FN=3, TN=77 → precision 60%, recall 80%.
- Client-side content contains the answer key and can be inspected. A browser-local score is **not a secure or independently proctored exam**.
- Written reflections have a length requirement; reasoning accuracy and true operator competence are ungraded.
- Supplement progress is kept in localStorage under `eh-multistage-assessments-2026-v1`. It does **not** use Firebase or update legacy lesson/exam state.
- External subject-matter review, live desktop/phone browser acceptance testing, accessibility testing, and academic equivalency sign-off are outstanding.

## Acceptance testing still needed
- Load hosted classroom via normal authenticated Academy and check level links on desktop and iPhone Safari.
- Select first case, submit one answer only (should block), enter <60 words (should block), supply both answers + >=60 words (should record feedback).
- Confirm later stages stay locked until predecessor submission and repeat through all four stages.
- Reload, switch cases, export JSON and verify submitted evidence persists in the same browser.
- Confirm no changes to original exam scores, courses, cloud progress or login behavior.
- Independently verify any actual security exercise is run only against explicitly authorized lab assets.

**Sign-off:** Internal structural review only. Not an external academic or technical certification.
