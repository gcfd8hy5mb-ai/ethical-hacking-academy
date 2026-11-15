# Batch 13 — Authorized Penetration-Testing Methodology and Enterprise Reporting

**Recommended study workload:** 12–16 hours, including independent writing and review. **Prerequisites:** Batches 8–12. **Environment:** downloaded Academy repository, Python 3, personal Windows/Linux machine or isolated VM. **Scope:** offline fictional assessment only; no live external targets, credential collection, exploit execution, third-party scanning or production changes.

## Course outcomes
A qualified security assessor needs more than a collection of tools. The goal is to decide what is authorized, understand the expected security boundary, identify defensible evidence, distinguish a vulnerability from an unsupported suspicion, design the least disruptive validation, communicate realistic risk, and specify a verified remediation. This unit develops those abilities in a fictional multinational enterprise.

## Module 1 — Rules of engagement and authorized assessment (2 hours)

A written assessment authorization should identify legal asset ownership, named approving authority, start/end times with timezone, permitted test types, prohibited actions, data handling, incident escalation contact, operational change windows and stop conditions. A host visible on the internet is not automatically an authorized target; possession of a technical capability does not confer consent. Activities beyond the agreed scope must not proceed.

**Worked scenario:** A corporate portal has a test tenant and a production tenant. The assessment letter authorizes only the fictional training evidence; it does not authorize the production endpoint, another employee's accounts or a partner's domain. A discoverable link is not permission to test it. If unexpected sensitive data are returned, stop, preserve minimally necessary evidence, notify the authorized contact and avoid further access.

**Independent deliverable:** Draft a one-page rules-of-engagement contract for a fictional assessment with four allowlisted targets, explicit prohibitions, a contact tree, data retention, severity escalation, and evidence handoff. Explain what to do upon encountering an out-of-scope asset.

## Module 2 — Asset and threat modeling (2 hours)

Model the principal, resource, trust boundary, expected permission, abuse hypothesis and defensive control. Separate authentication (who is acting) from authorization (what that subject may do to a specific object). A report identifier may be guessable yet harmless if the server enforces ownership; a hidden link is not a substitute for that authorization.

**Fictional worked case:** Tenant A's mock account obtains Tenant B's mock report. A server returned HTTP 200 in the supplied record. The finding is a *training fixture* cross-tenant authorization failure. The evidence does not support claiming real customer exposure. The defender should enforce server-side tenant and object checks and test both permitted and forbidden combinations.

**Independent deliverable:** Draw a trust-boundary diagram showing identity provider, application API, tenant-owned report data and audit log. Write four positive and negative authorization expectations, including an unauthenticated request. Explain why browser visibility controls do not enforce backend authorization.

## Module 3 — Evidence-based vulnerability validation (2–3 hours)

A strong finding contains observed result, expected result, repeatable test conditions, affected fictional asset, uncertainty and business consequence. The next step must fit explicit permissions and operational risk. Validation may include comparing response metadata against an approved expected outcome, but a single response does not establish attribution or exploitation.

**Four fictional assessment findings**
| Case | Observation | Plausible mechanism | Essential validation |
|---|---|---|---|
| Tenant isolation | A sees B's fictional report | Missing per-object policy | Cross-tenant deny and same-tenant allow |
| Sessions | Old fictional token still accepted after disablement | Session revocation gap | Old token deny; unaffected user allow |
| Configuration | 200 health but stale report | Application/config regression | Expected content after approved rollback |
| Backup | Job completed but integrity check failed | Recoverability unverified | Isolated restore and integrity verification |

Each finding requires evidence of its mechanism and a falsifying test. A backed-up file is not necessarily restorable. An account disabled for new login may still have an active session. An HTTP 200 can serve incorrect data.

**Independent deliverable:** For each case, write: scope, observation, expected state, leading hypothesis, one benign/alternative explanation, the safest authorized next check, a limiting factor, and a clear stop condition. Do not attempt live exploitation.

## Module 4 — Risk, prioritization and remediation (2 hours)

A ranking needs business context, not merely a vulnerability label. Evaluate exposure, exploit prerequisites, potential confidentiality/integrity/availability impact, compensating controls, likelihood uncertainty, and operational urgency. Separate findings from speculative attack chains; a perfect synthetic score cannot establish production impact.

**Example risk reasoning:** The fictional cross-tenant report exposure warrants high attention because it directly violates a data boundary, but an assessor must still acknowledge the synthetic nature of the observation. The stale-data regression might warrant medium priority in this model; if it affected critical transactions in a real business, its priority could be higher. Explain the chosen assumptions rather than presenting a universal severity.

**Independent deliverable:** Risk register with four findings, evidence quality, impact narrative, likelihood assumptions, remediation owner, target date, rollback and residual risk. Write a 150–250-word executive rationale for ordering the work.

## Module 5 — Test design and safe verification (2 hours)

Differentiate successful functionality from correct denial. A server-side fix is incomplete if it inadvertently blocks all valid use. Every authorization-sensitive repair should have at least one negative case and one positive case. A change must be reproducible in a disposable fixture before being proposed for production.

**Illustrative access validation**
| Principal | Requested resource | Expected |
|---|---|---|
| A | A's report | Allow |
| A | B's report | Deny |
| B | B's report | Allow |
| Unauthenticated | Private report | Deny |

**Illustrative recovery validation:** Compare the trusted backup digest, restore an isolated copy, verify record counts and sample integrity, test allowed/denied access, measure recovery time and record limitations. A check that the file merely exists is insufficient.

**Independent deliverable:** Ten-line positive/negative validation matrix, with test owner and evidence artifact for each. Identify the tests that would catch overbroad access grants, overbroad denials, data regressions and failed recovery.

## Module 6 — Executable offline assessment studio (2 hours)

The script does **not** scan or touch a target. It creates four fictional evidence cases and grades choices for **finding**, **validation**, **remediation**, and **priority**, then prints a structured report outline. Do your diagnosis before reading source answer keys, which are visible and make this an educational rather than tamper-resistant assessment.

From the repository root, initialize a **new nonexistent** workspace:

**Linux / WSL**
```bash
python3 local-vm-labs/batch13_assessment_reporting.py init --workspace "$HOME/academy-batch13"
python3 local-vm-labs/batch13_assessment_reporting.py inspect --workspace "$HOME/academy-batch13"
python3 local-vm-labs/batch13_assessment_reporting.py options
```

**Windows PowerShell**
```powershell
py -3 local-vm-labs/batch13_assessment_reporting.py init --workspace "$HOME\academy-batch13"
py -3 local-vm-labs/batch13_assessment_reporting.py inspect --workspace "$HOME\academy-batch13"
py -3 local-vm-labs/batch13_assessment_reporting.py options
```

Edit the generated `answers.json`. For each case, choose exact option identifiers and write at least 200 characters in `reasoning` and 40 characters in `out_of_scope`. These two free-text fields are checked for **length only**; a human must review their quality. Do not modify the synthetic `evidence.json` or `manifest.json`.

Grade and view the sample report outline:

**Linux / WSL**
```bash
python3 local-vm-labs/batch13_assessment_reporting.py grade --workspace "$HOME/academy-batch13"
python3 local-vm-labs/batch13_assessment_reporting.py report --workspace "$HOME/academy-batch13"
```

**Windows**
```powershell
py -3 local-vm-labs/batch13_assessment_reporting.py grade --workspace "$HOME\academy-batch13"
py -3 local-vm-labs/batch13_assessment_reporting.py report --workspace "$HOME\academy-batch13"
```

There are **16 objective selection points**, with an educational checkpoint at **13/16**. A changed evidence digest invalidates scores. A manifest within the same workspace is only an internal change detector, not a verified external evidence chain of custody. The generated report is a **template with explanatory findings**, not proof that any student's narrative has been independently assessed.

## Module 7 — Professional penetration-test report (3–4 hours)

**Final capstone:** Produce a 1,600–2,200-word security assessment for a fictional international retailer, with:
1. Engagement summary, authorization, legal/operational scope and exclusions.
2. Executive overview prioritizing business risks without sensationalism.
3. Four individually numbered findings with source identifiers and UTC timestamps (state when exact timestamps were not supplied rather than inventing them).
4. Expected/observed behavior and a competing hypothesis per finding.
5. Risk justification, affected trust boundary, recommended owner and change approval.
6. Least-disruptive remediation and rollback strategy.
7. Positive and negative post-fix validation with explicit success criteria.
8. Residual uncertainty, limitations and evidence-handling statement.

**Human-graded 30-point rubric:** authorization/scope (0–5); technical explanation (0–5); evidence and uncertainty (0–5); risk/business prioritization (0–5); validation/rollback completeness (0–5); report clarity and executive communication (0–5).

**Example of an acceptable conclusion:** “The fictional training tenant returned data belonging to another tenant despite the requester's intended restriction. A server-side authorization defect is the leading explanation in this controlled case; real-world exploitability is not established. A negative cross-tenant test and positive owner test are necessary after remediation.”

**Unacceptable conclusion:** “We hacked a major company and stole real customer information.” No such event occurred in this lab.

## Module 8 — Reviewer check and troubleshooting

**Developer regression command:**
```bash
python3 -m unittest discover -s tests -p 'test_batch13_assessment_reporting.py' -v
```
Windows may use `py -3` instead. Eight tests cover generated evidence, score limits, correct options, corruption detection, refusal to overwrite, report limitations and malformed answers.

**Common failures:** A preexisting workspace triggers refusal—choose a different disposable path. An invalid JSON answer file must be corrected with proper quotes and commas. A failed digest check requires preserving the modified file and creating an entirely new clean workspace, not doctoring the manifest. A perfect objective score does **not** mean that real cybersecurity work, independent reasoning or professional-level assessment has been certified.

**Compatibility:** No previous coursework identifiers, examinations, Firebase records, student grades, localStorage keys, or approved visual styles were modified. This is an appended optional training unit pending operational and editorial evaluation.
