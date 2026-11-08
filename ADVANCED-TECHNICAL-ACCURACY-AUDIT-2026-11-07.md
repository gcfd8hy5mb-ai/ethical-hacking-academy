# Advanced Workstations — Technical Accuracy Audit (2026-11-07)

## Scope
Reviewed the current browser-based advanced practical modules:
- `advanced-stateful-workstations.html`
- `advanced-randomized-fault-lab.html`
- `advanced-blind-troubleshooting-exam.html`
- `final-multifault-practical-exam.html`

This is an **internal source and structural check**, not independent expert sign-off or evidence that the simulations were tested on physical machines. No historical lesson, exam or Firebase keys were intentionally changed.

## Corrected finding: final practical did not distinguish observation before and after repair
**Prior behavior:** A fault inspection was counted toward exam evidence even if the student only inspected the simulated condition after it had already been fixed. This could inflate the evidence score.

**Remediation implemented:** The final practical now tracks:
1. Pre-repair observations of an active fault.
2. Simulated authorized repair (requires prior inspection).
3. Explicit after-repair verification by rerunning the corresponding inspection command.

The revised automated scoring weights are:
- Correct diagnoses: 4 × 8 = 32
- Authorized simulated repairs: 4 × 8 = 32
- Before-repair evidence inspection: 4 × 4 = 16
- After-repair verification: 4 × 2 = 8
- Simulated authorization: 12
- Total: 100, before the existing deduction of up to 20 points for unnecessary changes.

The provisional internal practical gate now requires all four correct diagnoses, four repairs, four before-inspections, four after-verifications, authorization, no unnecessary changes and at least 80 points. The minimum-length written report is **not** automatically evaluated for correctness.

## Compatibility
Previously stored local final-exam attempts are retained. Older attempts lack after-repair verification timestamps; they are migrated with an empty verification list and a legacy notice. Previously stored evidence is not treated as proven post-repair validation.

## Cross-module check
Static review confirmed browser-script syntax parsing for all four advanced modules and inspected the presence of local saving, simulated authorization, and reporting flows. Supported lab-only commands such as `lab repair ...`, `lab-switch ...`, `lab-iam ...` and `Set-LabDnsRecord` are **fictional simulator controls**, not real operating-system commands.

Command interpretation reminders:
- `ip route` reveals routing decisions, not application readiness.
- `systemctl status` reports a unit's state; successful startup does not guarantee an endpoint works.
- `journalctl` displays systemd journal entries, which require context and may be incomplete.
- `nginx -t` tests nginx configuration; it does not prove the service is running.
- `curl -I` requests response headers using HEAD; `curl -i` includes headers in a response to the normally used request method.
- `Resolve-DnsName` reports DNS results; an answer alone does not verify TCP/TLS/application correctness.
- `Test-NetConnection -Port` tests TCP transport connectivity; it does not validate an HTTP application or TLS identity.
- Simulated identity-role events are insufficient to attribute malicious intent without corroboration.

## Remaining review gates (not yet passed)
- Test every scenario and command sequence end-to-end in mobile Safari and desktop browsers.
- Exercise saved-data migrations and interrupted sessions on devices with real existing progress.
- Verify accessibility, keyboard interaction, export/download behavior and resilience to storage failure.
- Have an independent Linux, Windows, networking and incident-response reviewer check both correct and incorrect simulation outputs against real observed behavior.
- Validate learning outcomes through instructor-observed authorized labs; do not treat a browser result or self-report as professional certification.

**Overall status:** An identified scoring logic defect is corrected; structural checks passed. Independent technical accuracy review, live-browser acceptance testing and real-system practical sign-off are still outstanding.
