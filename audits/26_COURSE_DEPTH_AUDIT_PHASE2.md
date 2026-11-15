# 26-Course Depth Audit — Phase 2: Hardware and Identity Integration

**Date:** 2026-11-14. **Branch:** `coursework/batch8-independent-incident-response`. **Source:** full version 36 `curriculum.json`, read back as GitHub blob after in-place update.

## Actual modifications
- **20/20** Ethical Hacking Hardware Foundations lessons expanded in their existing lesson body fields. The additions are specific to each device or technical method, explain underlying interfaces and safety, present a bounded practice, interpret alternative explanations, and require a written independent assessment.
- **6/6** Digital Identity and Everyday Security lessons expanded in their existing lesson body fields with topic-specific security mechanisms, example decision paths, common failure interpretations and independent exercises.
- Course order, all lesson positions, question text, answer options, correct-answer indices and explanation fields were preserved during the JSON change.
- The accompanying `tests/test_core_curriculum_depth_integration.py` guard now checks the presence of the new 26 depth sections in addition to course counts and quiz shape. These guards have been committed but have not been independently confirmed passing in a Python test runner.

## Recalculated primary instructional body metrics

| Metric | After Phase 1 | After Phase 2 |
|---|---:|---:|
| Courses | 26 | 26 |
| Lessons | 198 | 198 |
| Approximate Unicode word tokens | 132,801 | 137,519 |
| Lessons under 500 words | 53 | 39 |
| Hardware lessons with new specific content | 0 in Phase 2 | 20 |
| Digital identity lessons with new specific content | 0 in Phase 2 | 6 |

The 500-word threshold is a **triage tool only**, not an educational quality grade. The expansions do not prove hands-on competence, independent grading or real-hardware operation. Device interaction remains optional and subject to ownership, legal limits, safety and explicit consent.

## Remaining short-lesson concentration

| Course | Short lessons |
|---|---:|
| Cybersecurity Foundations | 5 |
| Computer and Operating-System Essentials | 6 |
| Networking and Internet Fundamentals | 6 |
| Getting Comfortable With Computers | 5 |
| Cybersecurity Case Studies and Decision-Making | 6 |
| Applied Security Architecture and Threat Modeling | 5 |
| Practical IT Service Operations | 6 |
| **Total** | **39** |

**Next:** Expand the 39 remaining short core lessons with topic-specific mechanisms, worked examples, expected observable evidence, safe troubleshooting and independent evaluation. After that, perform a qualitative audit across all 198 lessons; longer lessons may still have gaps, repetition or weak assessment alignment.

## Pending verification before merge

1. Run the curriculum-depth regression tests and other Batch 8–15 GitHub Actions tests on Python 3.11/3.12.
2. Confirm iPhone and desktop lesson reader displays long-form instructional text without clipping, severe scrolling bugs or broken quiz states.
3. Verify no lesson/quiz progress moves when titles and bodies change; preserve the current positional storage keys.
4. Have a qualified reviewer assess accuracy, lab safety and skill assessment, especially radio, RFID/NFC, USB devices and security assessment methodology.
5. Evaluate real hardware separately rather than falsely counting text or tabletop exercises as physical competency.

No merge or production deployment was performed by this audit.
