# Batch 8 — Independent Defensive Investigation and Red-Team Reporting

**Level:** Intermediate to advanced | **Study plan:** 5 modules, about 8–12 hours of guided work plus written review | **Equipment:** Owned Windows/Ubuntu/WSL workstation, Python 3, text editor; no paid services.

**Purpose.** Progress from following a repair recipe (Batch 7) to defending a diagnosis against competing explanations. All example events, identities, hostnames, IPs, and access decisions below are fictional. Commands are read-only unless they explicitly create files inside a disposable folder. Do not test systems you do not own or have written authorization to assess. These exercises are local/offline; no scanning, exploits, credential collection, persistence, or third-party targets.

## Module 1 — Establish an evidence-preserving baseline (90–120 min)

### Theory
A security finding is a **claim supported by a reproducible observation**. Establish a timeline, the exact collection method, the scope of each evidence source, and what was not observed. Preserve original evidence separately from analysis. Hashes detect changed bytes, not who created a file or whether its assertions are truthful. A process name does not establish intent; a stopped service may be expected; a failed login is not necessarily an attack.

### Step-by-step Windows procedure (PowerShell, normal user)
```powershell
$lab = Join-Path $HOME 'academy-batch8'
New-Item -ItemType Directory -Path $lab -ErrorAction Stop
Get-Date -Format o
Get-ComputerInfo | Select-Object OsName,OsVersion
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name,Id,CPU
Get-Service | Select-Object -First 12 Name,Status,StartType
Get-NetIPConfiguration | Select-Object InterfaceAlias,IPv4Address,IPv4DefaultGateway
```
**Expected:** date with timezone offset, OS information, processes, service statuses, and available local interface data. CPU here is cumulative CPU time, not an instantaneous percent. Some commands may be unavailable under restricted PowerShell configurations; document the error rather than escalate privileges.

### Step-by-step Linux/WSL procedure (ordinary account)
```bash
date --iso-8601=seconds
uname -sr
id
ps -eo pid,comm,%cpu --sort=-%cpu | head -n 8
ip route show
ss -ltn
```
**Expected:** host metadata, account identity, process snapshot, routes and local listening sockets, subject to installed utilities and permissions. `ss -ltn` lists listening TCP sockets; it does not prove that an application is healthy, reachable remotely, or authorized. WSL may have different interface and service behavior from a standalone Ubuntu VM.

### Safe file integrity check
Create a **fictional** small text file in the Batch 8 disposable folder, save a separate copy and calculate SHA-256:
```powershell
'2026-11-14T10:00:00-06:00,training-user,denied,fictional' | Set-Content -Path "$HOME\academy-batch8\fictional-events.csv"
Get-FileHash "$HOME\academy-batch8\fictional-events.csv" -Algorithm SHA256
```
On Linux, create `~/academy-batch8` and a fictional-events.csv file, then run `sha256sum ~/academy-batch8/fictional-events.csv`. Alter one character in a **copy** and recalculate. The hashes should differ. Never overwrite an original evidence artifact to demonstrate tampering.

**Independent exercise:** Prepare a six-column evidence ledger: evidence ID, source, collection timestamp and timezone, acquisition method, integrity digest (if a file), and limitation. Give two alternative explanations for one process or socket. Explain why a digest does not authenticate a witness. **Deliverable:** evidence ledger and 300-word methods section.

## Module 2 — Windows event correlation without assuming compromise (90–120 min)

### Theory
A Windows event has a provider, event ID, time, host, and fields. Security log 4624 commonly denotes a successful logon and 4625 a failed logon, but logging policy, logon type, and context determine meaning. Correlation requires matching identities, time windows, relevant hosts, and whether an administrative change was authorized. Event counts alone are not an intrusion verdict.

**Read-only command when permitted:**
```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; StartTime=(Get-Date).AddHours(-2)} -MaxEvents 20 |
  Select-Object TimeCreated,Id,ProviderName,LevelDisplayName
Get-Service | Where-Object { $_.Status -eq 'Stopped' } | Select-Object -First 10 Name,StartType
```
**Expected:** recent system events (or an access/availability error) and stopped services. The `System` log is not the `Security` log, and a stopped `Manual` service is not automatically a failure. Do not modify audit policy or disable antivirus to obtain data.

### Fictional incident record
| Time (UTC) | System | Record | Interpretation candidate |
|---|---|---|---|
| 14:01 | workstation-A | User training-alex failed to sign in | Mistyped password or unauthorized attempt |
| 14:02 | workstation-A | Second failed sign-in, same user | Same two explanations still apply |
| 14:05 | workstation-A | Successful sign-in by training-alex | Could be legitimate after a typo |
| 14:08 | app-server-A | Training service stopped after approved release | Planned maintenance or regression |
| 14:12 | app-server-A | Application health HTTP 503 | Process exists but application cannot fulfill request |

**Worked reasoning:** The two failures at 14:01 and 14:02 do **not** prove credential stuffing. The 14:08 approved release makes a regression plausible; an HTTP 503 at 14:12 supports application unavailability, not DNS failure. Ask for the release record, sign-in source, and authenticated user session context before choosing a cause.

**Independent exercise:** Identify three claims supported by the table and three that remain unproven. Draft a prioritized investigation plan limited to read-only checks. **Deliverable:** 250–400 words plus a decision table (claim/evidence/counterexample/next check).

## Module 3 — Linux service and permissions triage (90–120 min)

### Theory
Distinguish account identity, ownership, mode bits, ACLs, process state, startup configuration, network binding and application health. A Unix `x` bit on a directory permits traversal; it does not mean executing the directory. `systemctl is-enabled` concerns startup configuration, while `systemctl is-active` concerns current state. Neither asserts end-to-end health.

**Read-only checks on an owned Linux VM:**
```bash
id
stat -c '%A %U:%G %n' "$HOME"
find "$HOME" -maxdepth 1 -type d -printf '%m %u:%g %p\n' | head
systemctl --user list-units --type=service --no-pager | head
ss -ltn
```
**Expected:** ownership/mode observations, optional user-service listing, listening sockets. On systems without systemd the unit command may fail. Do not recursively `chmod`, alter `/etc`, or change services as a workaround.

**Controlled paper case:** A fictional service running as `svc-report` must read `/srv/reports/public` but not `/srv/reports/private`. A proposed fix is `chmod -R 777 /srv/reports`. Reject the proposal: it broadens read/write/traverse permissions for everyone and affects private records. Design a least-privilege group/ACL remedy requiring an authorized administrator to approve and test it in a disposable fixture, with rollback instructions. Record exactly which principals need which rights and why.

**Independent exercise:** Make a permissions matrix for owner/group/others, expected read/traverse operations, risk of over-broad write rights, and test cases for allow/deny. **Deliverable:** permissions matrix and 250-word change advisory. This workbook does not authorize changing production permissions.

## Module 4 — Network / application fault isolation (120–150 min)

### Theory
Diagnose in layers rather than naming a threat from one symptom. A DNS timeout is a name-resolution problem; a TCP connection refusal often means there is no accepted listener at the addressed endpoint; HTTP 503 means the HTTP server responded but could not serve the request; HTTP 403 is a deliberate access refusal; HTTP 200 for a private resource may indicate an authorization defect if the requester lacked permission.

Use existing Academy **Batch 5 and Batch 6** localhost-only fixtures, not external hosts. In a new terminal after starting the two fixture services per their own workbooks:
```bash
python3 local-vm-labs/batch7_integrated_capstone.py
```
Windows users run `py -3`. Baseline fixture expectation is **6/14**, and after the separately documented allowed local repairs **14/14**, when both services are healthy; local environment differences can cause other results. The score measures fixture state, **not** independent attack-detection ability. Never turn a localhost-only server into a public listener.

**Evidence reasoning exercise:** For each hypothetical case—(A) name resolution timeout, (B) refused 127.0.0.1 connection, (C) 503 on the local service, (D) 200 on a fictional private URL without authorization—name the layer, what is proven, one alternative, and the next **authorized** observation. In D, distinguish server-side authorization enforcement from browser-side hiding and security headers.

**Independent exercise:** Write a fault-isolation decision tree and a four-row report with observed result, competing hypothesis, lowest-risk remediation, and post-fix negative test. **Deliverable:** tree, table and 300-word technical justification.

## Module 5 — Ethical red-team simulation, detection and board reporting (120–180 min)

### Scenario and engagement boundary
A fictional multinational retailer authorizes an **offline tabletop only** assessing its employee offboarding design, private document authorization and resilience to application failure. There are no real employee accounts, phishing messages, live targets or exploitable networks. Red-team thinking means modeling how a control could fail and how defenders would observe it; no attack execution is required.

### Three attack-path hypotheses
1. **Departed identity:** An access token might remain valid after employment ends. Controls to test in a **simulation**: revocation, session lifetime, and a negative access check.
2. **Cross-tenant private reports:** Client-side hiding could conceal a server-side authorization flaw. Defensive verification: distinct fictional tenants and a denied response for every unauthorized read.
3. **Availability degradation:** An approved configuration release could produce 503s. Defensive verification: change record, measured health before/after rollback, and corroborating telemetry.

### Threat and detection mapping
| Hypothesis | Asset at risk | Evidence required | Control owner | Safe verification |
|---|---|---|---|---|
| Stale token | Private records | Session revocation record and denied replay in simulator | Identity team | Synthetic negative authorization test |
| Cross-tenant access | Tenant reports | Principal/resource ownership and HTTP denial | App team | Separate fictional tenant fixture |
| Service regression | Availability | Approved change, health response and rollback evidence | Operations | Academy localhost test |

**Do not claim:** that an accepted request proves data theft, that a synthetic log confirms an actor, or that a perfect fixture score demonstrates a real intrusion. Privacy and contractual boundaries supersede technical curiosity.

### Written capstone: 1,200–1,800 words
Produce (i) scope and rules of engagement, (ii) asset/data-flow sketch, (iii) three evidence-backed hypotheses with falsifiers, (iv) detection and response plan, (v) lowest-risk fix and rollback for each, (vi) validation matrix containing at least three *negative* tests, (vii) residual risk, and (viii) a 200-word executive/board summary using nontechnical language.

### Twenty-point human review rubric
| Domain | Points |
|---|---:|
| Authorization and ethical boundary precision | 0–4 |
| Verifiable observations, provenance, counter-hypotheses | 0–4 |
| OS/network/web technical correctness | 0–4 |
| Least-privilege controls, rollback and negative tests | 0–4 |
| Clear, prioritized executive communication | 0–4 |

**Model of an acceptable finding:** “In the Academy’s fictional web fixture, a private resource returned HTTP 200 before server-side hardening. After applying only the approved local hardening command, the unauthorized request was denied. This demonstrates the behavior of the training fixture; it does not establish that a production system is vulnerable.”

**Model of an unacceptable finding:** “We proved the company was breached because there were failed logins and a 200 response.” The evidence does not support that conclusion.

## End-of-batch knowledge examination
Answer before comparing with the key.

1. What can a matching SHA-256 value establish about two files, and what can it not establish?
2. What is the difference between a TCP refusal and HTTP 503?
3. Does an HTTP 200 response prove server-side authorization was correctly enforced?
4. What extra context makes a 4625 failure meaningful?
5. Why is `chmod -R 777` a poor default permissions repair?
6. Differentiate `systemctl is-enabled` from `is-active`.
7. Why include negative tests in access-control validation?
8. What is the minimum evidence needed before alleging a malicious actor?
9. Which observations may be gathered safely on an owned workstation without modifying system state?
10. What remains unverified after the Batch 7 fixture reports 14/14?

### Answer key and grading rationale
1. Equal digests strongly support byte-for-byte identity under the algorithm; hashes alone do not establish source authenticity, chain of custody, or truthful content.
2. Refusal happens at the transport connection stage; 503 is an HTTP response from an endpoint that accepted a request.
3. No; 200 may expose an authorization defect when a principal should have been denied.
4. Logon type, source, account, host, timing, policy, related successes and expected user activity.
5. It grants unnecessarily broad access and risks private data; use scoped ownership/groups/ACLs.
6. Startup enablement versus present activity; neither validates a full transaction.
7. They establish that disallowed users/resources are actually rejected rather than merely hidden.
8. Corroborated, context-rich, attributable evidence and an explicitly bounded confidence statement; never infer malicious intent from a count alone.
9. Process/service, route, local listener and time snapshots when available; read-only visibility is not permission to collect another person's data.
10. Independent problem solving, real enterprise conditions, written explanation quality, and supervised hands-on proficiency.

**Scoring:** 1 point per correct answer with supporting explanation (10 possible); 8 is a study checkpoint, not a qualification. Misinterpretations should trigger repetition of the corresponding module. The written capstone is not automatically scored.

## Reviewer sign-off and safety
Record observed commands and outputs, environment/version, uncertainties, whether a trusted reviewer read the report, and any differences from the workbook’s illustrative outcomes. No certification, external review, live-target assessment or physical-device validation is implied. Keep local personal logs out of public repositories; redact credentials, hostnames and identifying data. Cleanup involves only reviewing and deleting the **disposable Batch 8** artifacts you created; never issue broad recursive deletion commands against unverified paths.

## Developer acceptance checks
- Existing 26-course lesson identity, examinations, navigation, approved visual design and student progress are untouched by this Markdown-only addition.
- The new Academy link is a normal document link; the browser does **not** run these shell or PowerShell commands.
- Check Windows and Linux commands on owned test systems before marking operational results verified.
- Have a knowledgeable reviewer assess the exam/capstone reasoning and authorization boundaries.
