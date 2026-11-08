# Lesson-Specific Fieldwork and Offline Evidence Review — Internal Audit
Date: 2026-11-08

## Authored in this batch
- Added 23 new individually authored exercises to `coursework-specific-practice-2026.json` (Windows process inspection, PC hardware selection/repair and home-lab engineering).
- Added 23 exact course-title and lesson-title associations; total mappings increased from 52 to 75.
- Modified `app.js` to combine the core practical catalog and specific practical catalog on demand within normal lesson screens.
- Incremented `index.html` script URL to `expanded-practice-v43-20261108`.
- Added `local-vm-labs/academy_evidence_review.py` with read-only constrained file checks and structured finding-note headings.
- Added WSL 1-compatible use instructions in `real-local-linux-lab.html`.

## Static verification completed
- All 75 authored mappings point to existing unit and section IDs across the two practice catalogs.
- All 75 mapped titles exist in the published four supplement sources (foundations, systems/red team, applied security, PC track).
- No duplicate mapping pairs identified.
- All 23 new exercises have instruction, result interpretation, learner task and safety boundaries.
- `app.js` parsed with an async-function JavaScript syntax check.
- Original app progress key remains unchanged; no original lesson indexes or exam data were deliberately altered.
- Linux review helper uses Python standard-library filesystem and hashing operations; network scanning and intentionally vulnerable services are not part of this script.

## Scope and quality limitations
- Existing `curriculum.json` primary catalog has not been fully inventoried because the GitHub file-content tool did not return its full body. Core-only unmatched lessons may remain.
- Every title is a verified structural match, but the quality of topic alignment is not externally peer reviewed.
- The new review script verifies file-state and note format, not reasoning accuracy, independence or operator proficiency. Its JSON output is learner-controlled and not a secure certificate.
- The read-only review script has not been executed in a real Ubuntu or WSL environment in this round; source retrieval for a local runtime test was unavailable. Python runtime compatibility and edge-case handling require test execution.
- Cross-browser acceptance, Firebase state persistence and academic equivalency reviews remain outstanding.
- WSL 1 may be used for basic local files and Python operations only; it is not a replacement for isolated vulnerable-target VMs.

## Recommended next acceptance tests
1. Load representative new exercises in the hosted regular lesson view and confirm content corresponds to the exact lesson title.
2. Rapidly change lessons while practice data fetches; verify old responses do not show in another lesson.
3. Complete an existing knowledge check and verify original completion behavior and cloud progress stay intact.
4. On WSL 1, run `python3 academy_lab.py setup`, then `python3 academy_evidence_review.py`; check expected failures before repairs.
5. Author the finding with OBSERVED:, UNKNOWN: and NEXT STEP: headings, correct file mode and config, rerun the reviewer and inspect `--json` output.
6. Verify symlinks and malformed/oversized files are safely refused, and verify no network activity or file modifications occur.

Status: GitHub commits and static mapping checks completed. Runtime, device and independent academic sign-off pending.
