# Batch 7 — Integrated Cybersecurity Practical Capstone

**Scope:** This capstone is an original, locally executable assessment involving Windows/Linux system evidence, real loopback HTTP troubleshooting, web access-control validation, fictional network telemetry, and written enterprise risk reporting. It is suitable for an owned computer or an isolated virtual machine. It is **not** a certified exam, a fully blinded practical test, or a substitute for independent technical evaluation.

## Prerequisites

* Download/clone the Ethical Hacking Academy repository and open a terminal at its root.
* Python 3 installed: Linux/WSL use `python3`; Windows PowerShell use `py -3`.
* No administrator account, third-party packages, real credentials or outside network target is required.
* Run the capstone on an explicitly authorized computer. All automated HTTP checks bind to and request from **127.0.0.1** only.
* Four terminal sessions are useful: two servers, one diagnostic terminal, one notes/evidence terminal. Both server programs are explicitly localhost-only.

## Part I — Start two independently controlled real HTTP systems

**Linux / Ubuntu / WSL, terminal A:**
```bash
python3 local-vm-labs/batch5_local_service.py init --workspace "$HOME/academy-capstone-service"
python3 local-vm-labs/batch5_local_service.py serve --workspace "$HOME/academy-capstone-service"
```

**Linux / Ubuntu / WSL, terminal B:**
```bash
python3 local-vm-labs/batch6_local_web_assessment.py init --workspace "$HOME/academy-capstone-web"
python3 local-vm-labs/batch6_local_web_assessment.py serve --workspace "$HOME/academy-capstone-web"
```

**Windows PowerShell:** use `py -3` instead of `python3`; use `"$HOME\academy-capstone-service"` and `"$HOME\academy-capstone-web"` for the workspace arguments. The two servers use different fixed ports, 18765 and 18766, and remain running in their respective terminals. If a workspace exists, the scripts refuse to overwrite it: do not delete or overwrite personal folders.

The initial state is intentionally degraded: the service is modeled unavailable with HTTP 503, while the web fixture exposes a **fictional** private resource and lacks selected defensive response headers. These faults do not exercise real OS account access controls.

## Part II — Baseline diagnostics (independent evidence)

In a third terminal, from the repository root:

```bash
python3 local-vm-labs/batch7_integrated_capstone.py
```

**Expected baseline objective score:** **6/14** — four deterministic synthetic-analysis checks, two accessible web-health/public checks, and zero healthy service checks. The report includes individual statuses, response bodies, the synthetic network-event summary and a fictional risk-priority sequence. It never writes to course progress or exams.

Before doing any repair, record your own hypothesis for each failure and explain whether the evidence proves an unavailable service, missing server-side access protection, incorrect data or a network problem. A 503 response is not the same as a refused connection; an HTTP 200 response is not evidence of secure authorization.

**Windows system evidence (read-only, normal PowerShell):**
```powershell
Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in 18765,18766 } | Select-Object LocalAddress,LocalPort,OwningProcess
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name,Id,CPU
Get-NetIPConfiguration | Select-Object InterfaceAlias,IPv4Address,IPv4DefaultGateway
```

**Linux system evidence (read-only):**
```bash
id
ss -ltn '( sport = :18765 or sport = :18766 )'
ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6
ip route show
```

Record actual output (redact user names, addresses and identifying details). A machine without `ss`, `ip` or the Windows networking cmdlets should document that limitation rather than disable security settings or install unapproved software. A listening port does not establish authorization correctness.

## Part III — Authorized repair and verified retest

In the diagnostic terminal, repair **only the two disposable local training configurations**:

**Linux / WSL:**
```bash
python3 local-vm-labs/batch5_local_service.py fault --workspace "$HOME/academy-capstone-service" --mode healthy
python3 local-vm-labs/batch6_local_web_assessment.py harden --workspace "$HOME/academy-capstone-web"
python3 local-vm-labs/batch7_integrated_capstone.py
```

On Windows use `py -3` and the equivalent Windows workspace paths.

**Expected after repair:** **14/14 objective fixture checks pass** when both servers are running normally:
- 3 actual service health/data checks;
- 7 real web HTTP status, response-content and header checks;
- 4 deterministic fictional network-evidence checks.

If the result is not 14/14, compare each failing check to the observed HTTP response. If the listener is gone, restart the server in your own terminal; do not disable local firewall or security protections to force a result. The synthetic event checks cannot confirm actual attack attribution or packet traffic.

## Part IV — Enterprise case analysis (written examination)

A fictional multinational retailer's internal checkout training system experiences intermittent service errors, an incorrectly accessible resource, and an event log with two denied connections and one DNS timeout. Produce a defensible written security memo addressing:

1. **Authorization and scope.** Define owned/approved assets, limitations, test times, what you did not access.
2. **Technical diagnosis.** Separate socket connectivity, HTTP 503, HTTP 403, HTTP 200 with invalid data, and client DNS problems. Cite local evidence.
3. **System administration.** Explain the observed process, listener and route status on your Windows or Linux machine.
4. **Risk and controls.** Explain why the observed fictional private route is a server-side authorization concern; clarify why security headers do not themselves enforce identity-based access. Interpret synthetic allow/deny/timeout telemetry without claiming compromise.
5. **Remediation and communication.** Specify a remediation owner, bounded change, rollback, verified retest, remaining uncertainty and a concise executive summary.

A human reviewer must examine the **quality and originality** of this report. The tool cannot accurately score it.

## Grading, limitations and sign-off

**Objective fixture subtotal: 14 points.** Each live service/web check or deterministic telemetry assertion is one point. The result measures the fixture state at the time of the check and can be reached by following the written steps: it does not independently demonstrate problem-solving.

**Written practical analysis: 20 points, not auto-graded.** Five categories, each 0–4: scope/provenance; OS observation; network reasoning; web authorization reasoning; remediation, retest and communication.

**Total possible composite: 34 points**, but a complete assessment requires an independent human evaluator and a previously unseen problem. A self-scored report or 14/14 on the fixture is not professional sign-off.

### Regaining control and cleanup

Use Ctrl+C in both server terminals. The tools never remove your workspace. Inspect the two disposable lab folders before manually removing them. Never point the exercises at another person's network or device. The application only links the workbook; personal machine evidence is not automatically synced to Firebase or stored in course progress.

### Developer verification

GitHub CI includes `tests/test_batch7_integrated_capstone.py`, using real loopback servers on OS-selected ephemeral ports. It checks degraded baseline, both repairs, a regression back to weak settings, and closed-service behavior. CI does not reproduce the student's environment or independently assess the written memo.
