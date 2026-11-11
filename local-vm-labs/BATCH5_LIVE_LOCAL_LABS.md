# Batch 5 — Hands-on local service, system diagnostics & independent competency

This is a real executable Python 3 lab that starts a **local-only HTTP service** on your own Windows, Linux, macOS, WSL or Ubuntu VM. It needs no packages beyond Python 3 and no admin rights. It deliberately introduces three controlled service faults, then checks the result with actual localhost HTTP requests. The service **does not** imitate a full DNS resolver, host firewall, or external network.

## Requirements and scope
- Use only a computer you own or have written authorization to administer. Never bridge a training VM to a network you do not control.
- Get the Academy repo ZIP or clone from GitHub. Open a terminal **at the repository root**.
- Linux/Ubuntu/WSL: use `python3`; Windows PowerShell: use `py -3`. Confirm with `python3 --version` or `py -3 --version`.
- Port 18765 must be available on **loopback**. The script always binds to `127.0.0.1`, never `0.0.0.0`. Local processes on the same computer can access the test endpoint; avoid putting secrets in the fixture.
- No production credentials, scans, elevated privileges, security-disabling commands, or external target requests are part of this lab.
- Run Python commands yourself locally: the website cannot execute them remotely and does not upload or grade your machine's evidence.

## Lab A — Real HTTP health diagnosis (45–60 min)

**Linux/Ubuntu/WSL terminal A**
```bash
python3 local-vm-labs/batch5_local_service.py init --workspace "$HOME/academy-batch5"
python3 local-vm-labs/batch5_local_service.py serve --workspace "$HOME/academy-batch5"
```

**Windows PowerShell terminal A**
```powershell
py -3 local-vm-labs/batch5_local_service.py init --workspace "$HOME\academy-batch5"
py -3 local-vm-labs/batch5_local_service.py serve --workspace "$HOME\academy-batch5"
```

Leave terminal A open. In a **second terminal** in the repository root, run the verifier:

**Linux terminal B**
```bash
python3 local-vm-labs/batch5_local_service.py verify --workspace "$HOME/academy-batch5"
```

**Windows terminal B**
```powershell
py -3 local-vm-labs/batch5_local_service.py verify --workspace "$HOME\academy-batch5"
```

**Expected initial observation:** `/health` and `/records` return **HTTP 503**, and `passed` is false. This is an active HTTP server intentionally returning unavailable, **not** the same as a refused TCP connection. If the server is not running, the verifier instead records a connection error with `status: null`.

**Why:** HTTP 503 indicates the server handled the request but its modeled service is unavailable. A connection refusal occurs before an HTTP response exists. Distinguish service status from routing, DNS and firewall hypotheses.

**Independent question:** Why is the HTTP status alone insufficient to determine the root cause of a real outage?

## Lab B — Repair and verify (30–45 min)

In terminal B, change **only the disposable lab's configuration** and rerun the verifier:

**Linux:**
```bash
python3 local-vm-labs/batch5_local_service.py fault --workspace "$HOME/academy-batch5" --mode healthy
python3 local-vm-labs/batch5_local_service.py verify --workspace "$HOME/academy-batch5"
```

**Windows:** use `py -3` with the same options and `"$HOME\academy-batch5"`.

**Expected:** `/health` returns HTTP 200 with `{"state":"ready"}`; `/records` returns HTTP 200 containing two synthetic `ok` records; all three verifier checks are true and `passed` is true.

**Why:** The verifier checks both HTTP status **and** exact response content, not merely whether a socket accepted a connection.

**Troubleshooting:** If an address-in-use error occurs, another local program is using 18765. Stop the other program if it is yours, or choose a free nonprivileged port such as 18766 using **the same** `--port` option for both `serve` and `verify`. If setup says workspace already exists, do not overwrite it: omit `init` or choose a different owned folder. A failed verifier is an observation, not permission to disable antivirus/firewall.

## Lab C — Three controlled defects (60–90 min)

Keep the original server running. Terminal B can change `service.json`; the server reads that file for every request.

1. `--mode stopped`: HTTP 503 for both endpoints. Distinguish from a server that is completely stopped (connection refused).
2. `--mode denied`: health is 200, records is 403. Investigate authorization/policy assumptions; the denial is a **simulated local application rule**, not Windows/Linux ACL enforcement.
3. `--mode bad-data`: both endpoints return HTTP 200, but the records have intentionally incorrect content. Explain why availability does not equal correctness.
4. `--mode healthy`: return to the verified baseline.

For each mode, rerun the `verify` command and save a **redacted** evidence sheet: predicted response/status, observed status, observed JSON, two plausible hypotheses, why one is better supported, a safe corrective action, and the outcome after recovery.

**Assessment:** Without looking at the previous command sequence, diagnose a mode selected by a lab partner on the same machine (with permission). Do not claim independent mastery if you knew the fault in advance.

## Lab D — Real Windows/Linux host observations (45–60 min)

These are **read-only system inspection** tasks. They do not change operating-system settings.

**Windows PowerShell**
```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name,Id,CPU
Get-Service | Select-Object -First 10 Name,Status,StartType
Get-NetTCPConnection -State Listen | Where-Object {$_.LocalPort -eq 18765} | Select-Object LocalAddress,LocalPort,OwningProcess
Get-NetIPConfiguration | Select-Object InterfaceAlias,IPv4Address,IPv4DefaultGateway
```
Expected: process details (CPU = cumulative seconds), a service sample, a listener on local port 18765 while your lab is running, and interface configuration. PowerShell availability or output may vary. A machine may show both IPv4 and IPv6 loopback or no listed listener depending on permissions/tools; record the observation without changing protections.

**Linux / WSL / Ubuntu**
```bash
id
ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6
ss -ltn '( sport = :18765 )'
ip route show
```
Expected: local account, process summary, a TCP listener bound to 127.0.0.1:18765 while the lab is running, and routing table (which may be empty in an isolated VM). Some minimal Linux installations lack `ss`/`ip`; report limitations rather than installing packages without approval.

**Independent tasks:** Identify the local listener and explain why the address matters; distinguish host routing state from the behavior of an already-running loopback server; provide one false conclusion a novice might draw from a successful /health check.

## Objective verification and rubric

The built-in verifier reports three boolean facts:
- `service_ready`: expected HTTP 200 /health body.
- `records_accessible`: HTTP 200 from /records.
- `records_exact`: body equals the two expected fictional records.

The three checks must all be true to record a **local fixture pass**. This measures known state, not how the student diagnosed the fault. Independently score a written explanation out of 100: environment/scope (20), prediction vs evidence (20), mechanism and correct diagnosis (20), troubleshooting/retest (20), limitations and safe report (20). For credible assessment, use a separate reviewer and a previously unknown fault.

**Cleanup:** Ctrl+C in terminal A stops the server. The script never deletes the training workspace; inspect it before manually deleting your own disposable folder. Never run these lab commands against outside IP addresses.

## Automated test and validation limits

`tests/test_batch5_local_service.py` starts an actual HTTP server on an OS-selected ephemeral **127.0.0.1** port. It checks the stopped, denied, bad-data, and healthy states; missing-listener behavior; and no-overwrite protections. GitHub Actions runs the tests where supported. Browser deployment only supplies the guide; it cannot validate your personal Windows/Linux machine.
