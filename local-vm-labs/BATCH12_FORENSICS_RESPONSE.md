# Batch 12 — Digital Forensics, Malware Triage, Containment and Recovery

**Suggested workload:** 12–16 hours. **Prerequisites:** Batches 8–11. **Equipment:** owned Windows/Linux computer with Python 3 and a text editor. **Safety:** No actual malware, suspicious executable downloads, real attack samples, reverse-engineering execution, remote targets or production changes.

## Learning outcomes
The learner will (1) preserve original evidence and record provenance; (2) distinguish static indicators from demonstrated malicious behavior; (3) assess a security alert against benign alternatives; (4) design proportionate containment; (5) verify that a backup can actually be restored; (6) confirm that revoked access is denied; and (7) communicate confidence and limitations. This is defensive training, not a certification or supervised live-forensics examination.

## Module 1 — Evidence collection, integrity and chain of custody (2 hours)
A forensic claim should identify its source, collection time and timezone, collection method, relevant system identity, analyst, expected baseline and uncertainty. A SHA-256 digest allows comparison of bytes against an earlier recorded digest, but it does not by itself establish the source's authenticity. Preserve the original artifact, investigate a copy, record every handoff and avoid making conclusions that exceed the evidence.

**Practical exercise:** Prepare a six-column evidence ledger (evidence ID, source, UTC collection time, analyst, digest, known limitation). Explain why a changed digest is a reason to investigate rather than definitive proof of an attacker. Discuss how timezone skew could reorder apparently related events. **Deliverable:** evidence ledger and 250-word provenance memo.

## Module 2 — Safe malware-analysis foundations (2–3 hours)
Malware triage is the examination of suspicious **indicators** before any claim of confirmed infection. Static analysis can consider metadata, filename-extension mismatch, signature information, claimed origin, a hash, embedded strings and document behavior requests. Dynamic analysis observes actual execution and requires controlled professional infrastructure; this batch intentionally does **not** execute unknown programs or provide active samples.

**Fictional training case:** A text-only invoice note urges staff to enable macros. This is a social-engineering warning sign, not executable malware. It does not demonstrate infection or provide a file hash for known malware. Alternative hypotheses include a badly designed legitimate document workflow or malicious lure. An appropriate defensive response would be to preserve the message, verify the sender through a trusted channel, check email telemetry under authorization, and avoid enabling macros.

**Worked reasoning:** “Urgent” is not technical proof. A suspicious instruction plus an unexpected attachment supports investigation priority. Actual execution would require process evidence, user testimony or trustworthy endpoint logs.

**Independent task:** Create a claim/evidence/alternative/falsifier table for five possible indicators. Draft a 300–450-word analysis clearly separating suspicious content, confirmed execution, persistence, and impact. Do not download real malware to complete the assignment.

## Module 3 — Windows and Linux forensic observations (2–3 hours)
On an **owned or explicitly authorized** Windows computer, the following are read-only examples:
```powershell
Get-Date -Format o
Get-Process | Sort-Object CPU -Descending | Select-Object -First 8 Name,Id,CPU
Get-WinEvent -FilterHashtable @{LogName='System';StartTime=(Get-Date).AddHours(-1)} -MaxEvents 10 |
 Select-Object TimeCreated,Id,ProviderName,LevelDisplayName
```
A process list is an observation, not proof that a process is harmful. Some event logs require additional permissions; do not weaken security or elevate privileges to force output.

On Linux or WSL:
```bash
date --iso-8601=seconds
id
ps -eo pid,user,comm,%cpu --sort=-%cpu | head -n 10
ss -ltn
```
Listening sockets do not prove remote reachability, and a process name does not prove parentage or intent. WSL observations differ from an actual Linux server.

**Fictional endpoint case:** A script interpreter alert overlaps a signed maintenance task. The alert justifies investigating process ancestry, authorization, command context, timestamps and reputable validation. It does not justify immediately declaring a compromised host.

**Independent task:** Produce a host-observation worksheet and explain two benign causes and two security concerns consistent with the same alert. Specify the minimal additional evidence needed to distinguish them.

## Module 4 — Incident containment and preservation (2–3 hours)
Containment reduces exposure while preventing avoidable evidence loss and business disruption. Analyze response choices by confidence, severity, scope, reversibility and authorizing role. Network isolation, account disablement and broad credential resets may have operational consequences and should follow an approved incident plan; this exercise does not execute them.

**Fictional decision:** A single suspicious email and no endpoint execution record should not automatically trigger a company-wide shutdown. Preserve the message and investigate its distribution first. A confirmed active compromise would justify a different containment decision under a designated response authority.

**Decision matrix:** For the four cases below, write the objective, containment owner, possible collateral impact, data preservation requirement, rollback and verification:
- Unexpected macro-related message (no confirmed execution)
- Endpoint alert with potential approved maintenance
- Backup with digest mismatch
- Departed employee's old session retaining access

**Independent task:** Write 350–500 words comparing cautious observation to urgent isolation, with clear escalation triggers.

## Module 5 — Backup trust, restoration and business continuity (2–3 hours)
Backups are useful only if authentic, intact, appropriately protected and restorable. A filename or dashboard showing “backup completed” does not establish recoverability. A digest mismatch means the examined bytes differ from the recorded reference, assuming trustworthy reference management; the underlying reason is not established. Production restore should not proceed until validation, authority and rollback are established.

**Fictional recovery exercise:** A backup is listed but verification fails. Design an *isolated* validation: preserve the original copy, check trusted metadata, run restore to an approved test environment, compare expected records, test access controls, document restoration time and escalate unresolved discrepancies. Avoid replacing an active production dataset as a learning exercise.

**Independent task:** Define RPO (maximum tolerable age of recovered data) and RTO (maximum tolerable recovery time), choose illustrative values for a fictional retailer and explain how a failed test restore changes the recovery plan.

## Module 6 — Access recovery, negative testing and closure (2 hours)
A disabled login does not guarantee existing bearer tokens are invalidated. For the fictional departed-user case, the desired outcome is that the **old synthetic session is denied**, while an unaffected authorized user can still access approved resources. Verification should test the denial and the valid access path, and evaluate propagation delay.

**Independent task:** Write a 250–400-word change plan specifying authorization, scope, session invalidation mechanism, before/after evidence, rollback, privacy-preserving audit trail and remaining uncertainty. Distinguish session revocation from password reset.

## Module 7 — Four-case interactive offline assessment

From the downloaded Academy repository root, use a new, nonexistent disposable workspace.

**Windows PowerShell:**
```powershell
py -3 local-vm-labs/batch12_forensics_triage.py init --workspace "$HOME\academy-batch12"
py -3 local-vm-labs/batch12_forensics_triage.py inspect --workspace "$HOME\academy-batch12"
py -3 local-vm-labs/batch12_forensics_triage.py options
```

**Linux/WSL:**
```bash
python3 local-vm-labs/batch12_forensics_triage.py init --workspace "$HOME/academy-batch12"
python3 local-vm-labs/batch12_forensics_triage.py inspect --workspace "$HOME/academy-batch12"
python3 local-vm-labs/batch12_forensics_triage.py options
```

The tool creates `evidence.json` (four **text-only** cases), a SHA-256 manifest and an empty `answers.json`. Inspect the evidence, then choose an exact allowed `diagnosis`, `contain` and `verify` value for each case. Write at least 200 characters of reasoning for each, including an alternative explanation. Do not alter the evidence file or manifest. The Python source includes answers for transparency, so the exam is **not tamper-resistant**.

To grade on Linux:
```bash
python3 local-vm-labs/batch12_forensics_triage.py grade --workspace "$HOME/academy-batch12"
```
On Windows use `py -3` and the Windows workspace. Objective scoring is **12 possible** (three selections × four cases), with a study pass at **10/12**. Written reasoning is checked for length only; a reviewer must judge accuracy. Editing evidence invalidates the score unless a new workspace is initialized. A manifest alone is not independent evidence authenticity.

## Module 8 — Professional incident-response capstone (2–3 hours)
**Assignment:** Prepare a 1,500–2,000-word incident-response memorandum for a fictional multinational retailer. Address all four training cases without claiming a real intrusion. Deliver:
1. A scope and authorization statement and evidence chain-of-custody table.
2. Four event timelines, each with a primary hypothesis, benign counter-hypothesis and falsifying evidence.
3. A malware-indicator triage that does not conflate suspicious text with executable code.
4. A containment decision tree with approvals, business impact and reversibility.
5. A clean backup-verification/isolated restore plan with RPO and RTO.
6. A session revocation plan with denied old-token and allowed current-user tests.
7. A 200-word executive summary, risk register, remaining uncertainty and follow-up owners.

**Human-reviewed 30-point rubric:** Scope and evidence provenance (0–5), technical forensics accuracy (0–5), alternative explanations and confidence (0–5), containment proportionality (0–5), restore/authorization verification (0–5), and executive reporting (0–5).

**Example acceptable conclusion:** “The fictional invoice request is suspicious and merits review, but no execution or compromise is demonstrated; preserve it and examine authorized endpoint/email telemetry before attributing activity.”

**Example unacceptable conclusion:** “The word invoice confirms ransomware was deployed.” The artifact contains no evidence for that claim.

## Verification and limitations
Run:
```bash
python3 -m unittest discover -s tests -p 'test_batch12_forensics_triage.py' -v
```
Use `py -3` on Windows. Seven regression-test methods cover initialization, fixture structure, blank and perfect answers, changed evidence, option integrity, and invalid submissions. The tests do not verify professional competence or actual malware safety outside this inert fixture.

**Progress and safety:** This batch writes only to a newly created disposable student workspace. It does not change existing lesson IDs, exam indexes, localStorage keys, Firebase records or production settings. No independent examiner sign-off is implied.
