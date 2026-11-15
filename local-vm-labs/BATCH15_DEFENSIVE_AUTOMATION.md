# Batch 15 — Practical Systems Assessment, Defensive Python and Vulnerability Management

**Study plan:** 12–16 hours of reading, independent technical exercises, and a reviewed final report. **Equipment:** owned Windows/Ubuntu/WSL workstation, Python 3, a text editor; no subscriptions, elevated rights, external targets, or paid AI services required.

## Objectives and authorization
This batch bridges the Academy's early workstation lessons and enterprise assessment coursework. Students should be able to gather read-only host observations, form alternative explanations, parse structured security data with Python, prioritize hypothetical vulnerabilities, define safe patch validation, and write evidence-based executive reports. **Only run real-machine commands on equipment you own or are explicitly authorized to assess.** The grading script creates and reads fictional JSON files; it does not access live systems, scan hosts, exploit vulnerabilities, or operate on student progress data.

## Module 1 — Windows evidence and baseline reasoning (2 hours)

### Technical foundations
Windows provides many layers of observable state: installed OS information, services, running processes, network interfaces, update history, and event logs. Treat these as snapshots in time. `Get-Process` reports a process and may report cumulative CPU seconds; it does not prove a process is malicious. `Get-Service` distinguishes running and stopped states but a stopped demand-start service may be expected. A network address is not an indicator of compromise by itself.

**Run in a normal PowerShell session on an owned Windows PC:**
```powershell
Get-Date -Format o
Get-ComputerInfo | Select-Object OsName,OsVersion
Get-Process | Sort-Object CPU -Descending | Select-Object -First 8 Name,Id,CPU
Get-Service | Select-Object -First 12 Name,Status,StartType
Get-NetIPConfiguration | Select-Object InterfaceAlias,IPv4Address,IPv4DefaultGateway
```

**Expected:** OS metadata, local process names, service states and interface information. Results vary by machine. If a cmdlet is unavailable, document the limitation. Do not turn off endpoint protection or grant new privileges simply to make a command work.

**Worked assessment:** A fictional workstation has a pending, approved patch and no evidence of exploitation. Its urgency depends on actual exposure, vulnerability severity, business criticality, compensating controls and maintenance windows—not on the mere existence of a patch. A responsible recommendation includes change approval, a restore point or rollback procedure, rechecking version state, and verifying that normal sign-in still works.

**Independent deliverable:** A baseline table recording command, observed field, significance, benign alternative and next verification. Produce a 250–400-word patch advisory that distinguishes *risk* from *confirmed incident*.

## Module 2 — Linux service identity and safe inspection (2 hours)

### Technical foundations
File access in Linux depends on effective UID, group membership, parent directory traversal and file permission modes or ACLs. Even if a file is group-readable, an inaccessible parent directory prevents access. Granting world write or recursively changing a production directory is generally a poor default. Diagnose first, seek authorization, and use the smallest change that meets the real business requirement.

**Read-only commands on an owned Linux/WSL system:**
```bash
date --iso-8601=seconds
id
ps -eo pid,user,comm,%cpu --sort=-%cpu | head -n 10
stat -c '%A %a %U:%G %n' "$HOME"
ss -ltn
```
**Interpretation:** `id` shows the identity and groups of the current shell, not necessarily the fictional service account. `stat` reports home-directory metadata; it does not prove permissions on a different application's paths. `ss -ltn` shows listening local TCP sockets, not application authorization or external reachability.

**Worked case:** A report service is denied traversal through a parent directory, and a technician proposes `chmod -R 777`. Reject the change because it exceeds business needs and risks exposing private data. Write an ACL/ownership proposal scoped to the service identity and parent path, including allowed-read and denied-read tests. Do not execute the proposal on a real production filesystem.

**Independent deliverable:** Owner/group/others matrix and a 300-word corrective-action memorandum that includes rollback and risks to other applications.

## Module 3 — Python defensive automation foundations (2–3 hours)

### Technical foundations
A safe security automation should have an explicit input contract, predictable output, bounded filesystem access, no hidden writes, meaningful errors, and tests. Python's `json`, `pathlib`, `hashlib` and `collections` can analyze structured evidence without touching third-party assets.

Consider the following **read-only, local** demonstration for a deliberately fictional JSON file:
```python
import json
from pathlib import Path
from collections import Counter

path = Path.home() / "academy-batch15" / "inventory.json"
data = json.loads(path.read_text(encoding="utf-8"))
print("Assets:", len(data))
print("Labels:", Counter(key.split("_")[0] for key in data))
```
**Expected:** four synthetic assets when the Batch 15 workspace was initialized at this location. The example does not identify actual installed applications or vulnerabilities. The `Counter` example shows grouping by a naming convention and has no claim to be a threat-detection algorithm.

**Security reasoning:** A file digest can reveal changed bytes relative to an earlier digest but cannot prove where the original file came from. Validate structured data types before trusting contents. Use normal accounts and avoid automations that silently delete or repair systems. A human must approve any operational change.

**Independent deliverable:** Annotate each Python line with what it reads, how a bad input could fail, and whether it modifies the operating system. Modify the script *in your own disposable lab* to count the training asset facts by item, without collecting real host data.

## Module 4 — Vulnerability management and prioritization (2–3 hours)

### Mechanism and risk
Vulnerability management consists of inventory, exposure analysis, technical validation, contextual prioritization, change approval, remediation, retesting and residual-risk documentation. CVSS-style severity is useful but cannot replace asset criticality and actual exposure. A high-severity weakness on an isolated test system may pose less business risk than a medium-severity weakness exposed to production workloads. Conversely, an authorization failure affecting customer records may need urgent attention despite being described in simple terms.

**Four fictional cases:** Windows endpoint with pending approved patch; Linux report service with overbroad proposed permissions; cross-tenant API authorization defect; backup whose integrity check failed.

| Asset | Central concern | Evidence-supported next step | Caution |
|---|---|---|---|
| Windows endpoint | Approved update pending | Schedule reviewed patch and validate regular sign-in | No exploitation established |
| Linux report service | Missing parent traversal | Review scoped ACL plus positive/negative checks | Do not make everything world-writable |
| Multitenant API | Unauthorized cross-tenant response | Enforce server-side per-object checks | UI hiding is not authorization |
| Backup system | Integrity check failed | Preserve copy and validate isolated restore | Completion notice is not recoverability |

**Independent deliverable:** Risk register with likelihood assumptions, affected business process, criticality, compensating controls, owner, change window, rollback and evidence required for closure. Write 300–500 words explaining why priorities may change in a real company.

## Module 5 — Guided offline assessment with objective checks (2 hours)

Clone or download the Academy repository and open the project root. Choose a **new directory that does not already exist**.

**Windows PowerShell**
```powershell
py -3 local-vm-labs/batch15_defensive_automation.py init --workspace "$HOME\academy-batch15"
py -3 local-vm-labs/batch15_defensive_automation.py inspect --workspace "$HOME\academy-batch15"
py -3 local-vm-labs/batch15_defensive_automation.py options
```
**Linux / WSL**
```bash
python3 local-vm-labs/batch15_defensive_automation.py init --workspace "$HOME/academy-batch15"
python3 local-vm-labs/batch15_defensive_automation.py inspect --workspace "$HOME/academy-batch15"
python3 local-vm-labs/batch15_defensive_automation.py options
```

The initializer creates three files only inside the disposable workspace: `inventory.json`, `manifest.json`, and `answers.json`. The training script refuses to overwrite an existing workspace. The inventory contains four fictional cases and a SHA-256 checksum reference. Study the facts, choose exactly one permitted `decision`, `validation`, and `priority` option for each case and enter those identifiers into `answers.json` with a text editor. For each case, add at least 200 characters in `reasoning` explaining two interpretations and why the preferred response is safer. The length field is **not** an evaluation of correctness.

Grade with:
```bash
python3 local-vm-labs/batch15_defensive_automation.py grade --workspace "$HOME/academy-batch15"
```
Windows uses `py -3` and `"$HOME\academy-batch15"`.

**Objective assessment:** 12 available points, three choices per case. A score of **10/12** is a provisional study checkpoint. The program rejects a modified inventory digest and does not auto-grade reasoning. Since Python source discloses the answers, the score cannot serve as a blinded practical examination or certification.

**Troubleshooting:** A pre-existing folder should not be deleted blindly; choose a new workspace. For JSON parse errors check double quotes, comma separators and exact identifiers. For evidence-integrity failures preserve the modified file and initialize a different workspace. The tool does not inspect real patches, users, networks or installed packages.

## Module 6 — Independent troubleshooting and validation design (2 hours)

Without re-reading the answer key, write a validation plan for an approved and isolated training service with four different problems: denied access, incorrect content, unavailable health endpoint, and a backup needing integrity verification. Explain why a successful HTTP 200 is different from valid data, why an HTTP 403 may be either an expected private-resource denial or an overbroad public-route rule, and why a failed digest check must trigger investigation.

Use a table with columns: intended control, baseline evidence, alternate explanation, allowed corrective action, positive test, negative test, rollback and unresolved uncertainty. This exercise is a written plan, not permission to target a live system.

## Module 7 — Enterprise practical capstone and professional report (2–3 hours)

Write a **1,500–2,000-word** fictional multinational-company cybersecurity memo. Include:
1. Authorized scope, safety boundaries, baseline evidence and provenance limitations.
2. Windows and Linux observations with no invented host results.
3. Four training risks ordered by exposure, operational impact and confidence.
4. Python data-handling explanation and why offline fictional outputs do not prove real weaknesses.
5. Approved remediation and rollback for each case.
6. A validation matrix including working positive and restrictive negative checks.
7. An executive summary under 200 words and a list of residual uncertainties.

**Human-reviewed 30-point rubric:** authorization/scope 0–5, Windows/Linux reasoning 0–5, data/automation integrity 0–5, risk prioritization 0–5, validation/rollback 0–5, and executive communication 0–5.

An acceptable claim is “The fictional evidence supports prioritizing server-side tenant authorization tests.” An unsupported claim is “We successfully exploited a production company.” No actual exploitation occurs in this batch.

## Developer regression checks and deployment limitations
Run from the repository root:
```bash
python3 -m unittest discover -s tests -p 'test_batch15_defensive_automation.py' -v
```
Windows can use `py -3`. Seven test cases verify fixture creation, blank and perfect assessment scoring, tamper detection, no overwrite, answer option coverage and malformed answer rejection.

The standalone lab does not change existing lesson identifiers, exams, Firebase records, cloud sync, previously saved workspaces or design files. Developer tests, student browser navigation, cross-platform commands and independent review must be verified before a merge-readiness claim.
