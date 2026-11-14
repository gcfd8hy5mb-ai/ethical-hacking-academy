# Batch 9 — Independent Incident Investigation and Practical Readiness

**Audience:** Ethical Hacking Academy students who completed Batch 7 and Batch 8. **Study workload:** approximately 10–14 hours of original instruction, command interpretation, synthetic assessments and a written report. **Equipment:** Windows, Linux, WSL or a disposable VM with Python 3. No subscriptions, cloud accounts, administrator privileges or third-party packages required.

This batch trains the transition from *following instructions* to *forming, testing, and defending hypotheses*. The included Python exercise is **an offline synthetic evidence grader**, not a penetration-testing utility or proof of technical qualification. All names, timestamps, routes and reports are fictional. Test only your own systems or explicitly authorized systems.

## Lab setup and independent assessment

Download or clone the Academy repository and open a terminal in its root directory. All commands operate on the student's local computer, never within the Academy website. Start with a workspace path that **does not exist**: the initializer refuses to overwrite existing directories.

### Windows PowerShell
```powershell
py -3 local-vm-labs/batch9_independent_investigation.py init --workspace "$HOME\academy-batch9"
py -3 local-vm-labs/batch9_independent_investigation.py inspect --workspace "$HOME\academy-batch9" --case windows
```

### Ubuntu, Linux or WSL
```bash
python3 local-vm-labs/batch9_independent_investigation.py init --workspace "$HOME/academy-batch9"
python3 local-vm-labs/batch9_independent_investigation.py inspect --workspace "$HOME/academy-batch9" --case windows
```

Use `--case linux`, `network`, `web` or `cloud` to see the other investigations. The program creates five fictional plaintext evidence files, a SHA-256 checksum manifest and an editable `answers.json` response template. **Inspect first and form your own diagnosis before opening the answer key in the Python source.** The source necessarily includes grading answers and is not tamper-resistant.

Edit `answers.json` in a text editor. For each case, copy one exact option from the corresponding `inspect` output into each of `diagnosis`, `action` and `verification`. In `reasoning`, explain your evidence, a competing hypothesis, what the record cannot establish, and your safe validation plan in at least 150 characters. The presence check for reasoning **does not measure correctness**.

Then run:
```bash
python3 local-vm-labs/batch9_independent_investigation.py grade --workspace "$HOME/academy-batch9" --json
```
On Windows substitute `py -3` and `"$HOME\academy-batch9"`.

**Expected on the initial blank template:** **0/15** with evidence intact. **Expected with all correct selections:** **15/15**. A passing objective checkpoint is **12/15**, but no written explanation or real-system skill is auto-certified. If evidence text changes, that case's three selection checks become invalid; do not modify original evidence files. Hashes only identify modification relative to the stored manifest. They do not establish authenticity because a user may also change the manifest.

## Investigation 1 — Windows: the difference between event correlation and attribution

### Learning outcomes
Describe the boundary among operating-system logon data, deployment audit records and application health evidence. Distinguish an approved change regression from an unsupported claim of credential theft. Report the confidence and missing evidence.

### Concepts and applied method
Security-event analysis begins with the question: *Which source directly records the phenomenon I am claiming?* A Windows logon event may identify the account and logon type but not prove intent. Windows event ID 4625 can signal a failed sign-in; 4624 can record a success. The app fixture uses simplified fictional observations—not real Windows Security log entries—and must not be interpreted as a forensic capture.

A disciplined analyst separates: (1) facts, (2) inferences, (3) alternatives, (4) next observations, and (5) actions requiring approval. An HTTP 503 means an HTTP service answered with an unavailable response. It does **not** mean the browser cannot resolve the host. Two unsuccessful logins followed by a legitimate success can result from a user mistyping a password.

### Optional read-only host observation (owned Windows PC)
```powershell
Get-Date -Format o
Get-Service | Select-Object -First 10 Name,Status,StartType
Get-WinEvent -FilterHashtable @{LogName='System'; StartTime=(Get-Date).AddHours(-1)} -MaxEvents 10 |
  Select-Object TimeCreated,Id,ProviderName,LevelDisplayName
```
**Expected:** timestamp, service inventory and possibly recent System events. An empty result, missing provider or insufficient privileges is an observation to document, not a reason to weaken security. Do not paste personal or employer log contents into a public repository.

### Independent written assessment
Provide a timeline of five fictional events, a confidence-ranked diagnosis, two competing causes, and a scoped verification proposal. Explain why a planned deployment plus a missing path is stronger support for regression than a pair of failed logins is for compromise. **Deliverable:** 300–450 words.

## Investigation 2 — Linux: service identities and least privilege

### Learning outcomes
Explain effective file access with directory traversal requirements, ownership, group membership and optional ACLs. Reject indiscriminate permissions broadening.

### Theory and demonstration
Reading `/training/public/report.txt` requires more than permission on `report.txt`: the service needs traversal permission through each parent directory. A `0700` parent blocks traversal for a process running as an unrelated service identity even if the report file itself is readable by a group. The correct solution should match the intended service identity, group and specific path—not make the entire tree world-writable.

**Read-only checks on your own Linux VM:**
```bash
id
stat -c '%A %a %U:%G %n' "$HOME"
ps -eo pid,user,comm | head -n 10
```
The home-directory mode shown is a local demonstration, not necessarily the mode of the fictional report-service parent. Never issue `chmod -R 777` as a repair. A Linux system lacking `stat -c` may require a different command syntax; document the platform.

### Worked authorization matrix
| Principal | Public report read | Private report read | Parent directory traverse |
|---|---|---|---|
| `svc-reports` | Allow | Deny | Allow on approved path |
| Authorized report editor | Allow + approved write | As specifically approved | Allow |
| Unrelated local account | Deny | Deny | Deny |

The matrix expresses intended policy, not a guarantee that ACLs currently enforce it. An authorized administrator should apply any actual permissions change through reviewed configuration management with rollback.

### Independent written assessment
Specify the proposed narrowly scoped permission or ACL change, the approval authority, a successful allowed-read check, an unauthorized denial check and rollback steps. Identify two ways a broad recursive change could expose confidential information. **Deliverable:** matrix plus 300–450 words.

## Investigation 3 — DNS versus sockets versus HTTP

### Learning outcomes
Distinguish name lookup, transport connection, an HTTP application response and an authorization failure. Avoid conflating a missing record with malware.

### Causal model
A user enters a domain name. The resolver maps it to a destination, a TCP handshake may establish connectivity, TLS may authenticate the endpoint, and the HTTP application decides whether to serve a resource. Different failure points require different evidence and repairs.

| Observation | Layer suggested | Does *not* establish | Best next authorized check |
|---|---|---|---|
| Resolver NXDOMAIN | DNS name resolution | Host was attacked | Compare known correct internal record |
| Connection refused | Transport/listener | DNS is broken | Check authorized local service listener |
| HTTP 503 | Application availability | Packet loss | Check application health and deployment evidence |
| HTTP 403 | Application authorization | Legitimate user access works | Validate principal/resource policy |
| HTTP 200 for forbidden resource | Possible authorization weakness | Exploitation or data theft | Negative server-side authorization test |

The lab's `portal.training.example` uses reserved fictional naming. **Do not resolve or scan arbitrary real domains to complete this exercise.**

**Optional owned-host checks:**
```powershell
Get-NetIPConfiguration | Select-Object InterfaceAlias,IPv4Address,IPv4DefaultGateway
```
```bash
ip route show
ss -ltn
```
These report local state only; they are not a direct experiment on the fictional incident. A route and an open port do not prove application behavior.

### Independent written assessment
Construct a five-branch troubleshooting decision tree. For each branch, state the evidence that would falsify the leading explanation, the least disruptive approved remedy and a precise post-fix test. **Deliverable:** decision tree and 350–500 words.

## Investigation 4 — Web: object-level authorization and negative testing

### Theory
Authentication establishes an identity; authorization decides whether that identity may act on the *particular resource*. A browser can hide a link but cannot enforce the server's ownership check. Security headers provide useful browser defenses but do not replace access-control logic.

The fictional case models Tenant A receiving HTTP 200 and another tenant's report. The supported inference is that the training fixture fails to enforce the expected per-object access rule. We cannot infer that a real customer was affected, that a malicious person accessed a report, or that a public endpoint exists.

### Four-case validation table
| Principal | Resource | Expected response | Why this matters |
|---|---|---|---|
| Authorized A | A's report | Allow | Positive functionality |
| Authorized B | B's report | Allow | Positive functionality |
| A | B's report | Deny | Cross-tenant negative test |
| Unauthenticated | A's private report | Deny | Identity boundary negative test |

Actual status conventions vary; a sound policy can use 403 or, to limit disclosure, 404. The crucial invariant is that private content is not returned to an unauthorized caller.

### Independent written assessment
Define a precise authorization rule using principal ID, tenant membership and resource ownership. Explain why a client-side filter is insufficient; give at least two negative tests and a rollback plan for a server-side policy update. **Deliverable:** policy pseudocode and 350–500 words. **No attack against a real website is required or authorized.**

## Investigation 5 — Cloud: token lifetime and offboarding

### Theory
An account can be disabled for new sign-ins while an already-issued bearer token remains valid. Security designs need to reason about session invalidation, token expiry, authorization changes and the delay until changes take effect. This differs from an assumption that a password reset invalidates all sessions immediately.

A correct negative test must attempt a **fictional previously authorized token** after the offboarding change and verify denial. A positive test should confirm that a separate currently authorized user can still complete the intended operation. Both checks matter: an overly broad policy that blocks everyone is not a successful remediation.

### Independent written assessment
Create a control design with token issuance, revocation, maximum lifetime, trusted authorization state, audit logging and rollback of misapplied policy. Include a timeline with initial account disablement, session invalidation and post-change retest. Specify which uncertainty remains if a system uses stateless tokens. **Deliverable:** 400–550 words plus an access-decision diagram.

## Advanced synthesis: incident response and red-team-informed defense

Assume the five investigations affect different training environments at an international company. You are the incident commander. There is no verified hostile actor. You must avoid calling every anomaly an attack, while still protecting high-value data.

**Phase 1 — Scope and authority:** Inventory the fictional host, service, report and session boundaries; list explicitly what cannot be tested.

**Phase 2 — Preserve evidence:** Maintain provenance of the five synthetic files and record any digest mismatch. Preserve the originals; analyze copies.

**Phase 3 — Competing hypotheses:** Use the Windows release record to distinguish regression from account misuse, the Linux permission layout to distinguish policy from process failure, and the DNS evidence to distinguish resolution from app health.

**Phase 4 — Controlled remediation:** Route each correction to its owner. Use least privilege, server-side object checks, and token revocation. No disabling security tooling or public access changes.

**Phase 5 — Retest and report:** Require a positive function test **and** a relevant negative test wherever access is involved. Report confidence, impact, uncertainty, recovery owner and residual risk.

### Written professional capstone (1,500–2,000 words)
Deliver an executive incident memo, technical appendix with five distinct diagnoses, evidence ledger with SHA-256 limitations, a risk-ranked remediation register, six negative/positive validation checks, and a plan for preserving business continuity. Clearly separate what was actually observed in the fictional case from what would have to be collected in a real authorized investigation.

### Independent reviewer rubric (25 points)
| Criterion | Points |
|---|---:|
| Ethical scope, evidence provenance and disclosure boundaries | 0–5 |
| Mechanistic accuracy across Windows/Linux/network/web/cloud | 0–5 |
| Alternative hypotheses, falsification and confidence calibration | 0–5 |
| Least-privilege fixes, rollback and positive/negative validation | 0–5 |
| Executive communication, risk prioritization and residual uncertainty | 0–5 |

A reviewer should provide paragraph-specific feedback, not only a number. The Python objective grade measures **three selected fields per case**—diagnosis, action and verification—only. **An 80% synthetic score does not certify actual Windows/Linux skill, incident handling, or independent red-team competence.**

## Optional supervised real-machine validation
A supervisor or self-reviewer can observe the student run **read-only** Windows/Linux host checks on an owned machine, explain each output without memorizing expected data, and state a safe follow-up. For professional readiness, the next batch should add a previously unseen, disposable, local service with injected faults and verifiable repair—not just a known synthetic answer key.

## Troubleshooting

- **`FileExistsError` at init:** Choose a fresh, clearly named disposable workspace. The script intentionally never overwrites an existing folder.
- **`FileNotFoundError` at inspect/grade:** Initialize with the same `--workspace` first and run from the repository root.
- **`JSONDecodeError`:** Validate that `answers.json` remains proper JSON (double quotes and commas); do not edit original evidence files.
- **`evidence_intact: false`:** A text file no longer matches its initial digest. Preserve the original evidence, stop grading that case and reinitialize a **new** separate workspace if you want a clean attempt.
- **0/15 after writing:** The grader accepts only exact option identifiers shown by `inspect`, not paraphrased answers.
- **No Windows PowerShell or Linux tools:** The offline Python examination works on either OS and does not depend on platform-specific utilities.

## Developer verification

Run from the repository root:
```bash
python3 -m unittest discover -s tests -p 'test_batch9_independent_investigation.py' -v
```
On Windows run with `py -3 -m unittest discover -s tests -p test_batch9_independent_investigation.py -v`. The tests cover fresh initialization, 0/15 baseline, 15/15 perfect answers, evidence modifications, response-shape handling, and answer option consistency. They cannot verify cross-device behavior, real professional reasoning, network environments or independent academic sign-off.

**Progress compatibility:** No existing curriculum IDs, exam indexes, Firebase records or localStorage keys are changed. The new evaluator reads and writes only its explicitly named disposable workspace. No merge or production deploy occurs simply because this file exists.
