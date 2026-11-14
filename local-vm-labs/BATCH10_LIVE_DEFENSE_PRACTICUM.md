# Batch 10 — Advanced Hands-On Red-Team / Blue-Team Defense Practicum

**Level:** Intermediate/advanced | **Suggested workload:** 12–16 hours including independent writing | **Equipment:** Own Windows or Linux/WSL computer or isolated VM; Python 3 standard library, no root/admin permissions. **No third-party services or subscriptions.**

## Purpose, scope and boundaries
Earlier batches taught command interpretation, scripted fixture repair and offline forensic reasoning. Here, a fresh, **unknown training fault** affects a *real running HTTP service* on **127.0.0.1 only**. The student must observe the failure, lock in a diagnosis, select a bounded remedy, verify positive and negative outcomes, and write a report that distinguishes observation from inference.

The embedded red-team component models adverse conditions and tests defender controls in a disposable system. It does not require or authorize external scans, exploit attempts, credential capture, phishing, malware, persistence or access to another person's device. This is a training fixture, not a production assessment. The source code contains the possible faults and therefore the exercise is not a securely blinded examination.

## Module 1 — Laboratory methodology and trust boundaries (2 hours)

A local service has multiple layers: TCP listener, HTTP application response, data accuracy, and security-policy handling. Investigate each independently. An opened listening port is not proof of a functional application. HTTP 200 is not proof that data are correct. HTTP 403 is meaningful only in the context of *which* resource and principal should be denied. A successful positive test never substitutes for a negative authorization test.

The training fixture exposes only:
- `/health`: fictional application readiness
- `/reports`: fictional public business records
- `/private`: fictional restricted training resource, always denied

All network operations use literal 127.0.0.1. The program never accepts an IP/host override. It stores only a randomly chosen case definition, one submitted diagnosis, and attempted synthetic repairs inside a fresh disposable folder.

**Evidence ledger:** Before remediation, record date/time, operating system, lab workspace, service port, relevant request, response status, response body, headers, your first hypothesis, one alternative hypothesis, and a limiting factor. Never publish your real host identity or unrelated system logs.

## Module 2 — Boot the disposable live service (2 hours)

Download or clone the GitHub project, then open a terminal at the repository root.

**Linux / Ubuntu / WSL — terminal A:**
```bash
python3 local-vm-labs/batch10_live_defense_practicum.py init --workspace "$HOME/academy-batch10"
python3 local-vm-labs/batch10_live_defense_practicum.py serve --workspace "$HOME/academy-batch10"
```

**Windows PowerShell — terminal A:**
```powershell
py -3 local-vm-labs/batch10_live_defense_practicum.py init --workspace "$HOME\academy-batch10"
py -3 local-vm-labs/batch10_live_defense_practicum.py serve --workspace "$HOME\academy-batch10"
```

The initializer refuses an existing directory; choose a distinct new workspace for another attempt. The real service binds only to local loopback on port **18767** (choose a different allowed port with `--port` if already occupied; use the same port with all subsequent commands).

**Linux / WSL — terminal B:**
```bash
python3 local-vm-labs/batch10_live_defense_practicum.py inspect --workspace "$HOME/academy-batch10"
python3 local-vm-labs/batch10_live_defense_practicum.py options
```

**Windows PowerShell — terminal B:**
```powershell
py -3 local-vm-labs/batch10_live_defense_practicum.py inspect --workspace "$HOME\academy-batch10"
py -3 local-vm-labs/batch10_live_defense_practicum.py options
```

**Expected observations:** Three JSON response records for `/health`, `/reports` and `/private`. The intentionally degraded fixture is randomly selected from:
1. **Availability fault:** health and report both respond 503.
2. **Public access fault:** health responds correctly but the public report yields 403.
3. **Integrity fault:** 200 response contains the wrong fictional report data.
4. **Caching fault:** a successful report response is missing `Cache-Control: no-store`.

The restricted `/private` route should return 403 in all four cases. A 403 on `/private` is a **desirable** negative test; a 403 on `/reports` is an undesired denial in this particular training policy.

**Troubleshooting:** A refused local connection means the HTTP server may not be running or the port differs. This is not an HTTP 503. Restart only your own training server or select a new free port, rather than disabling your firewall. A local VM or WSL may expose network details differently, but the tool itself never binds beyond IPv4 loopback.

## Module 3 — Independent diagnosis and scoped repair (2–3 hours)

Without reading `case.json` or looking up the fault answer in source, write:
- Two evidence-supported observations with exact status/payload/header references.
- One primary root-cause diagnosis and one competing hypothesis.
- A minimal training-only repair with authorization and rollback.

Run `options` to obtain exact diagnosis and repair identifiers. Then submit your **first** diagnosis, which cannot be revised:

```bash
python3 local-vm-labs/batch10_live_defense_practicum.py submit --workspace "$HOME/academy-batch10" --diagnosis service_unavailable
```

The command above is only an **example** for a 503 fault. **Choose the identifier warranted by your own observed result.** On Windows, substitute `py -3` and a Windows workspace path. Do not blindly submit the example.

Select exactly one scoped repair, for example:
```bash
python3 local-vm-labs/batch10_live_defense_practicum.py repair --workspace "$HOME/academy-batch10" --action restore_service_configuration
```

That action is appropriate **only** for the availability fault. The program rejects unknown repairs, tracks the number of attempts, and changes only the disposable lab configuration. A wrong repair leaves the fault in place and reduces a first-attempt scoring component. It does not alter Windows/Linux operating system settings.

**Red-team perspective:** State which observation a malicious actor might exploit *if a similar flaw existed in an authorized system*. Do not execute an attack. Describe how a defender could detect the situation and how a legitimate operator could verify whether the mitigation breaks normal use.

## Module 4 — Validate the real HTTP outcome (2–3 hours)

After remediation, re-run:
```bash
python3 local-vm-labs/batch10_live_defense_practicum.py inspect --workspace "$HOME/academy-batch10"
python3 local-vm-labs/batch10_live_defense_practicum.py grade --workspace "$HOME/academy-batch10"
```
Again, use `py -3` on Windows.

The objective grader checks seven conditions, weighted to ten points:
| Check | Points |
|---|---:|
| Correct first diagnosis | 2 |
| Correct repair applied | 1 |
| Exactly one repair attempt | 1 |
| Actual HTTP health endpoint responds 200 with expected state | 2 |
| Actual public report endpoint responds 200 with exact records | 2 |
| Cache policy explicitly returns no-store | 1 |
| Unauthorized private route actually returns 403 | 1 |
| **Total** | **10** |

A passing objective score requires **at least 8/10**, correct report data and a denied private route. A perfect result is 10/10 after an appropriate first diagnosis and first repair. Server-not-running behavior must fail live verification rather than be counted as successful.

**Important limitation:** There is no real identity system: `/private` always returns 403, and the public report is intentionally unauthenticated synthetic data. This lab demonstrates HTTP observations and bounded configuration changes, **not full object-level authorization testing or real adversarial activity**.

**Negative testing interpretation:** A private 403 response establishes that the fixture denied that route on this request. It does not prove that every hidden API endpoint is safe or that a real identity provider is correctly configured.

## Module 5 — Analyst report and incident command (3–4 hours)

Treat the incident as a fictional subsidiary outage/security-control concern. Write a 1,200–1,800-word report organized into:

1. Scope, written authorization assumptions, and exclusions.
2. Pre-repair evidence ledger with exact responses and timestamps.
3. Your locked initial diagnosis; alternative hypothesis and why it is weaker.
4. The one permitted repair and its least-privilege, reversible nature.
5. Actual post-change JSON output; required positive and negative checks.
6. What the live grader objectively proves and what it does **not** prove.
7. Two potential monitoring signals for early detection in a real enterprise.
8. Residual risk and an executive summary under 200 words.

**Expected reasoning examples:**
- An HTTP 200 payload with `state: incorrect` illustrates data integrity failure even while transport and HTTP status function normally.
- A 503 is an application-layer response rather than evidence of a DNS failure.
- A missing `Cache-Control` policy can represent an application-response hardening issue, but the exact caching risk depends on data sensitivity, cache behavior and deployment architecture.
- A public route returning 403 may represent an erroneous policy, while a private route returning 403 can represent proper denial.

### Professional report rubric — human graded (30 points)
| Criterion | Points |
|---|---:|
| Authorized scope and evidence integrity | 0–5 |
| Technical precision and plausible alternatives | 0–5 |
| Least-disruptive remediation and rollback | 0–5 |
| HTTP status, payload, header and negative-test interpretation | 0–5 |
| Detection engineering and business impact | 0–5 |
| Executive communication and limitations | 0–5 |

The written report is not evaluated by the Python program. Independent review and a genuinely unfamiliar external practical challenge are still required before any claim of professional competency or certification.

## Student reflection and extension

After finishing one case, create a **different** fresh disposable workspace and repeat without checking the previous answer key. Compare what evidence changed and what remained constant across faults. The Python source contains all four possible fixtures; this is a learning practicum rather than a tamper-resistant exam.

As an advanced *defensive-only* extension, write a small threat model for the training service: assets (public synthetic report and deliberately denied private route), trust boundary (loopback-only HTTP), threats (incorrect routing, service outage, incorrect data, unsafe caching), detective controls (health and content checks), and preventive controls (bounded allowlisted repairs, no public binding, no real credentials).

## Automated developer regression

From project root:
```bash
python3 -m unittest discover -s tests -p 'test_batch10_live_defense_practicum.py' -v
```
Windows equivalent:
```powershell
py -3 -m unittest discover -s tests -p test_batch10_live_defense_practicum.py -v
```

Seven test methods check the four distinct real HTTP faults, correct diagnosis/fix scores, wrong repair, first-diagnosis locking, never-overwrite init, missing-server failure and unknown routes. The tests run their own loopback server on an ephemeral OS-chosen port and never access outside hosts. Passing automated tests would validate controlled fixtures, not live enterprise proficiency.

## Safety, clean-up and progress

Press Ctrl+C in terminal A to stop the service. Review the explicitly chosen **disposable** Batch 10 workspace before manually removing it. Never issue a blanket recursive deletion command against an unverified path. No progress, grades, Firebase records, installed apps, firewalls, system users, production services or third-party systems are changed by the tool.

**Developer status:** The code and workbook are suitable for review, but operational readiness must be determined by executing tests on Windows/Ubuntu and checking student browser navigation. No independent academic review has occurred.
