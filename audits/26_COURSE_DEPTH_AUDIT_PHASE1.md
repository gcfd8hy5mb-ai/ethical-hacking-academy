# Ethical Hacking Academy — 26-Course Depth Audit, Phase 1

**Source:** `curriculum.json` version 36 on development branch `coursework/batch8-independent-incident-response`. The audit inspected the complete JSON blob, not the README alone. **Date:** 2026-11-14.

## Verified primary-curriculum baseline
- **26 courses and 198 authored lessons** (including the 20-lesson hardware foundations course).
- **Approximately 130,190 instructional words** in the primary lesson body fields, using Unicode word-token matching; separate workbooks, additional lab files, exam banks and simulations are excluded.
- **69 of 198 lessons have fewer than 500 words** using this repeatable tokenization method. Different word counters can return slightly different results.
- Every lesson has a body; a word count and the presence of “practicum” do **not** demonstrate academic depth, correctness or a functioning graded lab.
- Existing quiz/checkpoint structure and lesson positional identifiers must be preserved during expansions; do not reorder the JSON lesson arrays.

## Course-by-course register

| # | Course | Lessons | Core words | <500 words |
|---:|---|---:|---:|---:|
| 1 | Cybersecurity Foundations | 6 | 2,922 | 5 |
| 2 | Computer and Operating-System Essentials | 6 | 2,812 | 6 |
| 3 | Networking and Internet Fundamentals | 6 | 2,799 | 6 |
| 4 | Security Operations and Incident Response | 6 | 3,579 | 0 |
| 5 | Getting Comfortable With Computers | 6 | 2,844 | 5 |
| 6 | Beginner Linux and Terminal Skills | 8 | 6,594 | 0 |
| 7 | Digital Identity and Everyday Security | 6 | 2,659 | 6 |
| 8 | Windows Administration and Security | 8 | 6,398 | 0 |
| 9 | Networking Practice and Troubleshooting | 8 | 6,499 | 0 |
| 10 | Programming Logic for Security Beginners | 8 | 5,743 | 0 |
| 11 | Security Analysis and Professional Practice | 6 | 4,111 | 0 |
| 12 | Defensive Web and Cloud Fundamentals | 6 | 4,156 | 0 |
| 13 | Cybersecurity Case Studies and Decision-Making | 6 | 2,822 | 6 |
| 14 | Applied Security Architecture and Threat Modeling | 6 | 2,860 | 5 |
| 15 | Practical IT Service Operations | 6 | 2,709 | 6 |
| 16 | Introduction to Defensive Cryptography | 6 | 4,251 | 0 |
| 17 | Security Monitoring and Log Analysis | 6 | 4,859 | 0 |
| 18 | Safe Authorized Assessment Methodology | 6 | 4,842 | 0 |
| 19 | Hands-On Network Reasoning Workshop | 6 | 2,930 | 6 |
| 20 | Beginner Python Logic and Defensive Automation | 6 | 5,342 | 0 |
| 21 | Enterprise Identity and Access Management | 10 | 7,320 | 0 |
| 22 | Linux System Administration Lab Theory | 10 | 9,205 | 0 |
| 23 | Web Application Security Fundamentals | 10 | 9,196 | 0 |
| 24 | Cloud Infrastructure Security | 10 | 8,426 | 0 |
| 25 | Security Assessment and Reporting Workshop | 10 | 4,242 | 10 |
| 26 | Ethical Hacking Hardware Foundations | 20 | 10,070 | 8 |
| **Total** | | **198** | **130,190** | **69** |

## Priority ordering

**Tier A — Advanced course depth and independently evaluated practice**
- Course 25, Security Assessment and Reporting Workshop: all 10 lessons around 413–435 words; high-priority improvement because it is intended to teach professional evidence-based assessments.
- Course 26, Ethical Hacking Hardware Foundations: 8/20 lessons below 500 words; original README confirms simulated hardware exercises do not establish device competence. Keep regulatory and consent rules.
- Course 19, Hands-On Network Reasoning Workshop: 6/6 lessons below 500 words and the name implies hands-on practice; add owned-device networking exercises with safe expected output.

**Tier B — Foundation and applied practice**
- Courses 1, 2, 3, 5, 7, 13, 14, 15: many lessons below 500 words. Deepen mechanisms, worked examples and troubleshooting, with course-specific rather than repeated generic prompts.

**Tier C — Longer core bodies, still requiring content evaluation**
- Courses 4, 6, 8–12, 16–18, 20–24: word count threshold passed, but no conclusion about accuracy, test alignment, textbook equivalence or real practical competence follows. The 10-course practical workbook series and independent review should be mapped to exact lesson outcomes.

## What counts as curriculum complete

1. **Every one of 198 lesson positions inspected** for accurate terminology, theory, evidence, worked example, troubleshooting, independent task and counterargument appropriate to its difficulty.
2. **Assessments aligned to lesson objectives:** examine quiz coverage, exam distractors, explanations, remediation and answer-key leakage; correct missing depth.
3. **Working practical verification:** actual tests with outputs on owned Windows/Linux devices and in browsers, with human review of written/practical reasoning.
4. **Curriculum traceability:** every workbook/capstone maps to intended course and lesson positions, not just a navigation link.
5. **Regression and progress safety:** automated test results recorded; all 26 course titles, 198 lesson positions, progress keys and existing scores preserved through any edits.
6. **External review separately labeled:** neither this internal audit nor word count qualifies as independent academic/professional sign-off.

**Important:** Word length is a triage indicator rather than a graduation target. Adding generic filler to reach 500 words would not make a lesson academically complete.

## Next development action

Expand Course 25's ten distinct topics, then integrate supplements into the actual course teaching flow without shifting existing lesson positions. Subsequent audits should target network workshop and hardware course, followed by foundation and advanced peer-review sampling. Record word counts and real independent assessments after each change, not just batch numbers.
