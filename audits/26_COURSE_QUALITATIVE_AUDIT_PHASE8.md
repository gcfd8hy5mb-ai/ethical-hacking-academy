# Ethical Hacking Academy — Qualitative Editorial Audit Phase 8

**Branch:** `coursework/batch8-independent-incident-response`  
**Scope:** Direct primary curriculum replacement of 30 generic teaching sections, with original course/lesson positions and quizzes preserved.

## Actual work

| Course | Lessons rewritten | Topic-specific coverage |
|---|---:|---|
| Windows Administration and Security | 8 | User/profile identities, paths, updates, services, NTFS access, Defender and firewall, Event Viewer, recovery |
| Networking Practice and Troubleshooting | 8 | Topology, addressing, CIDR, DHCP, DNS, ports, safe diagnostics, segmented access |
| Programming Logic for Security Beginners | 8 | Data flow, variables, types, conditions, loops, functions, records, static code review |
| Beginner Python Logic and Defensive Automation | 6 | Script tracing, synthetic event lists, type validation, functions, data sensitivity, validation |
| **Total** | **30** | |

Each changed section has a **distinct, topic-specific technical mechanism**, worked explanation, documented uncertainty and an independent task. Commands are read-only in the described optional owned-computer exercises; assessment workflows do not access unapproved systems or student accounts.

## Post-commit source checks

The complete updated JSON was re-fetched from its GitHub blob after commit `e0e841348c75e4e60d55d0ae03324cb6b082d6d8`.

| Metric | Prior | Current |
|---|---:|---:|
| Primary courses | 26 | **26** |
| Primary lessons | 198 | **198** |
| Lessons containing one of two tracked repeated templates | 84 | **54** |
| Lessons below 500 approximate Unicode word tokens | 0 | **0** |
| Approximate main lesson words | 135,230 | **133,936** |
| Correct-answer distribution by option index | 66 / 65 / 67 | **66 / 65 / 67** |

The lower word count reflects replacing mass-repeated instruction, not a claim of reduced curricular breadth. Word count alone is not an academic-depth measure.

**Progress and quiz integrity:** At update time, all original lesson titles/positions, question prompts, choice arrays, answer indexes and explanations were compared against the pre-change JSON and preserved. No Firebase changes, production merge or deployment were made.

**Regression tests:** `tests/test_core_curriculum_depth_integration.py` now guards all 30 updated lesson bodies and existing course/quiz structure. These checks were committed but their execution has not yet been confirmed.

## Remaining work

The **54 still-template-bearing lessons** are concentrated in the other foundational and intermediate courses. Each requires a careful technical edit; replacing text solely to make a template counter zero would be insufficient.

Examination quality remains a separate task: **24 examinations with 175 questions**, all core courses named by at least one exam, but objective-by-objective rigor and independent practical competency have not been established. Windows/Linux real-computer verification, iPhone/desktop lesson rendering, CI test execution and independent technical review remain outstanding.

## Next priority

Finish targeted editorial cleanup of the other 54 marked lessons while maintaining or improving evidence quality. Then run the entire test suite and an actual device-based curriculum acceptance matrix before any merge.

**Status:** Development-only authored content and static source verification. Not yet a confirmed professional-equivalent, fully tested or independently signed-off academy.
