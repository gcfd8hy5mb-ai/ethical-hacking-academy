# Batch 14 — Enterprise Security Architecture, Identity and Red-Team/Blue-Team Defense

**Suggested study workload:** 12–16 hours, including original reading, a stateful training simulator, independent exercises and a human-reviewed capstone. **Prerequisites:** Batches 8–13 or comparable Windows/Linux, network and security fundamentals. **Environment:** personal Windows/Linux/WSL workstation, Python 3, no paid tools.

## Purpose, authorization and limits

This batch teaches how enterprise defenders reason about identities, roles, application trust boundaries, network zones, allowed business flows and actionable detections. It uses a **fictional six-node graph**, four controlled policy settings and synthetic detection records. No attack execution, remote access, packet collection, real enterprise network configuration, credentials or exploitation occurs. Red-team thinking is represented by modeled control-failure hypotheses; blue-team work consists of defense, monitoring and safe validation.

By completion, students should be able to define least privilege, explain why segmentation and resource authorization differ, design positive and negative tests, identify likely false positives and give an executive a supported risk conclusion.

## Module 1 — Enterprise identity and directory concepts (2 hours)

Enterprise identity systems bind users and workloads to principals, groups, roles and credentials. A directory service such as Active Directory can provide centralized identity and group management, but successful authentication does **not** imply authorization for an arbitrary resource. Role membership may be inherited, nested or changed while sessions remain active. Privileged operations need explicit eligibility, constrained administrative workstations, auditability, review and revocation.

**Worked fictional situation:** A helpdesk principal can reach a privileged admin function without task-specific approval. This is an excessive-privilege concern in the simulator. The proper defensive design separates ordinary support and privileged administration, verifies role assignment, requires approved elevation where applicable, logs the decision, and checks that ordinary support work still succeeds.

**Independent assessment:** Create a role matrix for employee, contractor, helpdesk, app service, finance analyst and administrator. For each role, identify business needs, permitted systems, denied systems, approval authority and review frequency. Explain two ways a seemingly small inherited privilege creates a path to sensitive records. Use fictional role names, never real credentials.

## Module 2 — Segmentation, lateral-path reasoning and Zero Trust (2–3 hours)

Network segmentation groups systems and controls connectivity. It reduces reachability and blast radius, but an allowed network route must **not** substitute for application authorization. A company might separate user endpoints, application services, finance data and privileged administration into zones with explicitly approved cross-zone flows. A successful TCP connection tells you only about transport, not whether the business operation is authorized.

A threat-path model connects a starting principal, allowed connection, inherited permission, resource and possible harmful outcome. For defensive planning, identify the edge whose removal breaks the unwanted path while retaining business operations. No live movement between systems is required or permitted.

**Fictional graph:**

| Node | Business function | Intended relationship |
|---|---|---|
| contractor | Limited outside worker | Limited application access |
| employee | Internal user | Normal application access |
| helpdesk | Support role | No standing admin privileges |
| app | Application workload | Finance access only through approved service identity |
| finance | Restricted records | No arbitrary cross-zone reads |
| admin | Privileged interface | Access only through approved privilege controls |

**Worked decision:** The fictional app can read finance data without service authorization. A suitable improvement uses a narrow service identity and access policy, plus segmented connectivity and a denied negative test. Blocking every connection would reduce risk but break legitimate business transactions; secure design requires both boundary denial and retained approved flows.

**Independent assessment:** Draw two graph paths: one approved normal transaction and one hypothesized unsafe path. Identify the exact control that interrupts the unsafe path, relevant detection telemetry, one false positive and a rollback plan.

## Module 3 — Red-team hypotheses and blue-team control design (2 hours)

An ethical red-team assessment starts with authorization and a hypothesis about how a system *could* violate an intended trust boundary. A blue-team response translates that into preventative controls, measurable logging, and validation. Neither a proposed attack path nor a synthetic allowed edge proves a real organization is vulnerable.

**Four linked hypotheses:**
1. Excessive helpdesk privilege might allow unapproved admin actions.
2. A service without an explicit finance authorization boundary might access restricted records.
3. A contractor whose application role is too broad might cross a business boundary.
4. Overly strict hardening might block an ordinary employee's legitimate work.

For each, students should write the prerequisite, possible impact, expected negative/positive test, owning team and residual uncertainty. Do not translate fictional graph analysis into unsolicited testing of real directories or networks.

## Module 4 — Hands-on stateful policy practicum (2–3 hours)

The Python simulator maintains four fictional policy controls and four corresponding detection observations in a fresh disposable workspace. It performs **no real host/network changes**.

From the cloned/downloaded repository root, use a new nonexistent directory.

**Linux / Ubuntu / WSL**
```bash
python3 local-vm-labs/batch14_enterprise_architecture.py init --workspace "$HOME/academy-batch14"
python3 local-vm-labs/batch14_enterprise_architecture.py inspect --workspace "$HOME/academy-batch14"
python3 local-vm-labs/batch14_enterprise_architecture.py controls
```

**Windows PowerShell**
```powershell
py -3 local-vm-labs/batch14_enterprise_architecture.py init --workspace "$HOME\academy-batch14"
py -3 local-vm-labs/batch14_enterprise_architecture.py inspect --workspace "$HOME\academy-batch14"
py -3 local-vm-labs/batch14_enterprise_architecture.py controls
```

The initial graph intentionally has unsafe access decisions and prevents an ordinary employee's approved application flow. **Expected baseline score: 0/8.** Before changing anything, record each access result, which trust boundary it implicates and the alternative explanation that would need investigation in a real enterprise.

Now use each `enable --control <identifier>` operation from the displayed allowlist to model a narrowly scoped defense. For example, after determining that the fictional helpdesk role should not have admin access:

```bash
python3 local-vm-labs/batch14_enterprise_architecture.py enable --workspace "$HOME/academy-batch14" --control deny_helpdesk_admin
```

This is a **fictional setting**, not a real Active Directory ACL, firewall rule or group policy. On Windows use `py -3` and the Windows workspace. Use `inspect` after each change and describe the before/after access decision. Apply the other controls needed for appropriate finance, contractor and legitimate employee access.

For each control, use `record --event <identifier>` from the tool's allowed synthetic event list. Example:

```bash
python3 local-vm-labs/batch14_enterprise_architecture.py record --workspace "$HOME/academy-batch14" --event privileged_access_denied
```

A recorded event without its associated effective control does **not** count as successful detection. This avoids a simplistic “logs exist, therefore we are secure” assessment. In a real platform, logs would need source integrity, correlation, time synchronization and alert routing, none of which the simulator implements.

Finally:

```bash
python3 local-vm-labs/batch14_enterprise_architecture.py grade --workspace "$HOME/academy-batch14"
```

Use the equivalent Windows prefix/path on Windows.

**Objective rubric: 8 points.** Four valid access-control decisions and four corresponding synthetic evidence records, one point each. Expected after appropriate controls and records: **8/8**. A perfect score shows a student configured a deterministic toy model. Source code discloses solutions; the assessment is not blinded, and the program does not prove operational skill on real directory or networking systems.

## Module 5 — Detection engineering and SOC handoff (2 hours)

Effective detection design requires a source, condition, scope, event identity, time window, false-positive analysis, owner and response procedure. A denied privilege event may be a normal rejected user mistake, not a confirmed malicious action. A successful employee transaction is important evidence that a restrictive control is not simply denying everyone. A good analyst avoids equating failed requests with hostile intent.

**Synthetic detection-design matrix:**

| Detection | Expected trigger | Benign alternative | Analyst next step |
|---|---|---|---|
| Privileged denial | Helpdesk denied admin request | Mistaken request or stale workflow | Validate request authorization and role |
| Finance boundary denial | App workload denied unsupported finance access | Misconfigured approved service | Check approved service mapping |
| Contractor policy denial | Contractor attempts out-of-scope resource | Old role assignment | Review contract and entitlement |
| Normal business allowed | Employee accesses application | Ordinary work | Confirm the service remains functional |

**Independent assessment:** For each rule, write a short analyst playbook, two ways to reduce false positives, required retention and privacy restrictions, and when the event would trigger escalation.

## Module 6 — Enterprise hardening and change safety (2 hours)

Security changes need an approved change ticket, current baseline, business owner, test environment, rollback and evidence after release. A narrow rule is better than indiscriminate denial when the business requires an allowed path. Where a zone, role or service mapping is uncertain, do not change production based only on theoretical risk.

**Independent assessment:** Draft a change plan that contains four controls, four negative/positive test cases, logs to watch, a two-stage rollout and a fallback if the employee application transaction fails. Explain the distinction among preventative controls, detective controls and recovery controls.

## Module 7 — Comprehensive enterprise architecture capstone (2–3 hours)

Write a **1,500–2,000-word** assessment memorandum for a fictional multinational retailer. Include:
1. An engagement scope statement with explicit prohibition on real targets.
2. A diagram of the six principals/services and four authorized/unsafe edges.
3. A least-privilege role design with expected deny/allow decisions.
4. A minimal segmentation policy and an application resource-authorization layer.
5. A red-team-style hypothesis for each risk and the blue-team defensive response.
6. Four synthetic detection playbooks and false-positive limitations.
7. Evidence from your initial and final simulator results, with no invented real-world measurements.
8. An executive summary, residual-risk register, owners, rollback and positive/negative testing.

**Human-reviewed 30-point rubric:** scope/ethics 0–5; architecture correctness 0–5; identity/authorization reasoning 0–5; safe validation and change management 0–5; detection evidence and uncertainty 0–5; executive reporting 0–5.

**Model response:** “The fictional helpdesk-to-admin edge was initially allowed and became denied after an allowlisted training policy change. This illustrates least-privilege design but says nothing about real directory exposure. A production implementation would require an independently authorized entitlement audit and negative testing.”

**Weak response:** “We hacked Active Directory and proved the company is compromised.” Neither happened.

## Verification and known limits

Developer tests:
```bash
python3 -m unittest discover -s tests -p 'test_batch14_enterprise_architecture.py' -v
```
On Windows use `py -3`. Eight tests cover the 0/8 baseline, 8/8 fully configured policy, controls without telemetry, telemetry without controls, invalid inputs, refusal to overwrite a workspace and restricted output structure. Such tests verify application logic, **not** a live enterprise.

**Progress:** This workbook and script introduce no lesson-ID changes, grading migrations, Firebase writes or alterations to previous workspaces. All learning actions are confined to a newly created disposable folder. Technical peer review and genuine Windows/Linux/identity integration remain prerequisites for professional skill validation.
