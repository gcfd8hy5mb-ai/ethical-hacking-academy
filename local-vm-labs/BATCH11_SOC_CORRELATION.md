# Batch 11 — Security Operations Investigation: Windows, Linux, Networks and Cloud

**Depth target:** 12–16 hours of reading, independent reasoning and technical exercises. **Prerequisite:** Batches 7–10 or equivalent foundations. **Tools:** Python 3, a text editor and an owned Windows/Linux machine or VM for optional read-only observations. This workbook uses only original fictional evidence.

## 1. Professional goals and operating boundaries

At the end of this batch, the student should be able to distinguish what a source *recorded* from what an analyst *infers*, align events across hosts and time, identify plausible failure mechanisms, design minimally invasive confirmation steps, write a defensible incident report, and communicate uncertainty to executives.

**Rules:** There is no live third-party target, credential harvesting, system penetration or scanning. The Python exercise never collects real host logs or sends network traffic. Optional commands later in this workbook are read-only and limited to machines the student owns or is explicitly authorized to inspect. Do not upload personal or employer event logs to a public GitHub repository.

## 2. Start the four-case evidence laboratory (1–2 hours)

From the Academy repository root, choose a disposable workspace that does **not** exist. The script refuses to overwrite a directory.

**Windows PowerShell**
```powershell
py -3 local-vm-labs/batch11_soc_correlation.py init --workspace "$HOME\academy-batch11"
py -3 local-vm-labs/batch11_soc_correlation.py analyze --workspace "$HOME\academy-batch11"
py -3 local-vm-labs/batch11_soc_correlation.py options --case release_regression
```

**Linux, Ubuntu or WSL**
```bash
python3 local-vm-labs/batch11_soc_correlation.py init --workspace "$HOME/academy-batch11"
python3 local-vm-labs/batch11_soc_correlation.py analyze --workspace "$HOME/academy-batch11"
python3 local-vm-labs/batch11_soc_correlation.py options --case release_regression
```

**Expected:** 16 fictional JSONL events, 4 investigations, a SHA-256 manifest, and an editable `answers.json`. The `analyze` command summarizes source counts and groups the evidence by case. Events use UTC timestamps. **No command above inspects the real operating system.**

Read the evidence and record a hypothesis before consulting the source code, which necessarily contains answers. The four cases are `release_regression`, `linux_permission`, `dns_record`, and `session_revocation`. Run `options --case <name>` for available responses.

Edit `answers.json` with exactly one allowed identifier in each case's `diagnosis`, `next_check`, and `safe_action` fields. Write at least 200 characters in `reasoning` covering observations, two possible causes, why one is better supported, and residual uncertainty.

**Linux/WSL grading command**
```bash
python3 local-vm-labs/batch11_soc_correlation.py grade --workspace "$HOME/academy-batch11"
```
**Windows grading command**
```powershell
py -3 local-vm-labs/batch11_soc_correlation.py grade --workspace "$HOME\academy-batch11"
```

**Scoring:** 12 objective selection points; at least 10 for the synthetic knowledge checkpoint. The grader checks written explanation *length* but does not determine whether its reasoning is correct. If the evidence file's digest no longer matches the original manifest, the tool rejects objective success. A checksum establishes change relative to a saved manifest, **not** independent provenance or authenticity.

## 3. Windows timeline and event semantics (2–3 hours)

**Case:** An authorized deployment was followed by a missing service path and an HTTP 503. The timeline also includes one failed sign-in.

**Theory:** Event 4625 can represent an unsuccessful Windows logon; 4624 can represent a success. Event details, logon type, source workstation, time and expected behavior matter. An isolated failure does not establish an attacker. A System-log service message and an application deployment record are different sources and must not be conflated.

**Optional owned Windows workstation observations**
```powershell
Get-Date -Format o
Get-Service | Select-Object -First 12 Name,Status,StartType
Get-WinEvent -FilterHashtable @{LogName='System'; StartTime=(Get-Date).AddHours(-2)} -MaxEvents 20 |
  Select-Object TimeCreated,Id,ProviderName,LevelDisplayName
```
A command may return no events, unsupported-field errors or permission errors. Record the limitation instead of weakening security or escalating rights. A stopped manual service is not automatically suspicious.

**Worked diagnostic method:**
1. Establish whether the service is answering HTTP and whether its response is 503 versus connection refusal.
2. Locate the approved change record and compare the modified configuration path against its documented target.
3. Build a timeline with timezones and source provenance; avoid assuming causation from a sequence alone.
4. Treat the failed sign-in as a separately unproven concern unless account, origin and context corroborate it.
5. Propose rollback to the approved configuration only within an authorized disposable test fixture, then validate an application transaction.

**Independent assessment:** Write a 350–500-word causal analysis, including a competing credential-abuse hypothesis and the precise evidence that would make you revise your confidence.

## 4. Linux service identities and permissions (2–3 hours)

**Case:** A fictional report-service account cannot traverse a parent directory. The report file itself has a nominally readable group mode.

**Mechanism:** Access to a nested file depends on permission to traverse each parent directory plus permissions on the file. Process UID/GID and supplementary groups matter; a `0700` directory owned by someone else prevents traversal by the service. `chmod -R 777` does not solve the governance problem: it creates unnecessary access, including write rights.

**Owned Linux/WSL read-only exercises**
```bash
id
stat -c '%A %a %U:%G %n' "$HOME"
ps -eo pid,user,comm | head -n 12
ss -ltn
```
**Expected:** account identity and groups, home-folder permission metadata, process identities and any listening TCP sockets. The specific values depend on the system and may differ in WSL. These commands do not show the fictional service's actual permissions; distinguish example reasoning from actual host findings.

**Independent assessment:** Construct a permission matrix for approved report readers, writers, service identity and unrelated users. Specify exactly where traversal and read permissions are necessary. Propose a narrowly scoped ACL or group change for administrator review, one positive read test, two negative access tests, and a rollback. Include an alternate explanation such as a service-account mismatch.

## 5. Network fault isolation and DNS (2–3 hours)

**Case:** A fictional training hostname returns NXDOMAIN. A direct owned mock-service health check returns 200, and an authorized DNS change remains pending.

**Mechanism:** DNS lookup failure does not prove a TCP refusal, which does not prove an application returned a 503. A DNS configuration error can coexist with a functioning application listening at an address. Not all NXDOMAIN observations establish the same root cause: check the expected zone, record type, resolver view and change history.

**Owned machine checks**
```powershell
Get-NetIPConfiguration | Select-Object InterfaceAlias,IPv4Address,IPv4DefaultGateway
```
```bash
ip route show
ss -ltn
```
These commands inspect local configuration. They do not test arbitrary internet hosts. Do not run scans, edit DNS or disable a firewall to make a lab score pass.

**Decision table**
| Observation | Direct inference | Competing explanation | Next bounded check |
|---|---|---|---|
| NXDOMAIN | Resolver says name does not exist in that view | Typo or split-horizon policy | Compare intended approved record |
| Connection refused | Target socket did not accept connection | Service stopped or wrong port | Inspect owned listener |
| HTTP 503 | HTTP endpoint answered unavailable | Upstream dependency or maintenance | Check health and change record |
| HTTP 403 | Route denied request | Deliberate policy, possibly overbroad | Validate principal-resource rules |
| HTTP 200 with wrong content | Server answered but content invalid | Stale cache or wrong data pipeline | Compare expected schema and source |

**Independent assessment:** Write a decision tree that narrows resolution, routing, transport, HTTP and application data without naming an attacker. Give a corrective change, rollback and a post-fix verification step for each class.

## 6. Identity/offboarding and session revocation (2–3 hours)

**Case:** A fictional account is disabled and new password logons are blocked, yet an old synthetic token can still read a report.

**Mechanism:** Authentication is not the same as authorization of an already-issued session. Some tokens remain usable until expiry or until an enforceable revocation control takes effect. Detection must capture not just login attempts but access decisions for existing tokens without unnecessarily recording sensitive token values.

**Safe design procedure:**
1. Record an authorized offboarding event and a separate session invalidation event.
2. Define maximum token lifetime and server-side entitlement checks.
3. Deny the old synthetic token when requesting a protected fictional report.
4. Confirm a different valid user retains approved access (positive test).
5. Log decision time, application version and policy result without exposing token contents.
6. Explain any propagation delay or cache that limits revocation speed.

**Independent assessment:** Draw the lifecycle of a fictional issued token. Include issuance, normal access, employee disablement, revocation, old-token denial and continued access for an unaffected user. Explain why disabling the password login alone is insufficient evidence of logout.

## 7. Detection engineering across sources (1–2 hours)

A useful detection specifies: observation source, matching identity or host, event window, aggregation rule, expected benign background, threshold, likely false positives, and permitted analyst response. A rule such as “two failed logins = ransomware” is indefensible. Instead, articulate a narrower rule for *investigation prioritization* and clearly distinguish it from a confirmed incident.

**Proposed conceptual rules:**
- Correlate app 503 shortly after an approved configuration change **plus** service error evidence; investigate regression, not automatically compromise.
- Identify permission-denied errors for a service principal **plus** a recent service-account or ACL change; escalate to the service owner.
- Correlate NXDOMAIN for a known internal hostname **plus** approved zone updates; verify resolver configuration.
- Alert on protected-resource access from a synthetic session **after** an account disablement and attempted revocation; verify enforcement with negative tests.

**Independent assessment:** For each, specify the false-positive conditions, missing logs, time synchronization assumptions and privacy-minimizing retention policy.

## 8. Professional investigation report and capstone (2–3 hours)

Prepare a **1,500–2,000-word** fictional multinational-company incident packet with:
- Scope and rules of engagement, evidence custody and limitations.
- Four incident timelines and competing diagnoses.
- The actual 16-event source breakdown and manifest integrity result.
- A risk-ranked remediation register with owner and rollback.
- Six verification cases, including negative authorization checks.
- A 200-word board summary that distinguishes service continuity from access-control risk.
- A declaration that no actual host, enterprise account, customer information or real incident was investigated by the fixture.

### Human-review rubric (30 points)
| Dimension | Points |
|---|---:|
| Scope, authorization, provenance, time normalization | 0–5 |
| Windows/Linux mechanisms and technical correctness | 0–5 |
| Network/identity reasoning and counter-hypotheses | 0–5 |
| Minimal-remediation plans and positive/negative validation | 0–5 |
| Detection logic, false positives and evidentiary limits | 0–5 |
| Executive communication, priority and residual risk | 0–5 |

**Worked exemplary conclusion:** “The training records associate an approved change with a missing service path and HTTP 503. This supports a configuration regression hypothesis, but does not establish causation or rule out a coincident issue. The next step is to compare the approved change against the current configuration and verify a bounded rollback in the isolated fixture.”

**Unacceptable conclusion:** “The login failures prove the network was hacked.” The available evidence does not justify an attribution claim.

## 9. Operational checks and troubleshooting

- If `init` reports an existing workspace, choose a new disposable directory; never overwrite or delete a personal folder.
- If `answers.json` fails to parse, fix JSON punctuation and retain exact choice identifiers.
- If a manifest mismatch is reported, preserve the original synthetic evidence and begin a *new* workspace rather than secretly editing the manifest.
- The `options` command reveals allowable identifiers, not automatically the explanation or optimal choice. The source code itself is inspectable, so scores are educational and not tamper-resistant.
- No real SIEM agent, Windows event collector, Linux journal reader, packet capture or network service is launched.

## 10. Developer verification and graduation limitations

From repository root:
```bash
python3 -m unittest discover -s tests -p 'test_batch11_soc_correlation.py' -v
```
Windows: replace `python3` with `py -3`.

The seven test methods examine fixture generation, SHA-256 integrity, four-case grouping, initial and perfect grading, option consistency and refusal to overwrite or accept a malformed answer payload. These are development tests, not assessment of a student's ability to respond to a real incident.

**Compatibility:** The new script uses only disposable files. Existing 26-course lesson ordering, examination indexes, Firebase progress, prior Batch 9/10 workspaces and visual design remain untouched. Real-machine independent evaluation, technical editorial review and deployment tests remain required before completion/sign-off claims.
