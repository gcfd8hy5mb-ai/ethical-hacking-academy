# Batch 6 — Authorized Security Operations Labs

This workbook combines **real local HTTP behavior**, **offline network evidence**, safe vulnerability triage and professional reporting. Use only a computer or VM you own or are expressly authorized to administer. Nothing here authorizes scanning another person's computer, external websites, Wi-Fi networks or corporate systems.

## Setup and platform

Download the Academy repository ZIP from GitHub, open a terminal in the repository root and confirm Python 3. On Windows PowerShell use `py -3` instead of `python3`. On Linux/WSL/macOS use `python3`.

The web lab binds **only 127.0.0.1** (localhost). It is not publicly accessible through the internet or your LAN by default. Other processes on your own device can contact it, so never use real passwords or sensitive data. No third-party Python libraries, administrator permissions or real accounts are required.

## Lab 1 — Local HTTP application and authorization audit (60–90 minutes)

**Terminal A** on Linux/WSL:
```bash
python3 local-vm-labs/batch6_local_web_assessment.py init --workspace "$HOME/academy-batch6"
python3 local-vm-labs/batch6_local_web_assessment.py serve --workspace "$HOME/academy-batch6"
```

On Windows PowerShell:
```powershell
py -3 local-vm-labs/batch6_local_web_assessment.py init --workspace "$HOME\academy-batch6"
py -3 local-vm-labs/batch6_local_web_assessment.py serve --workspace "$HOME\academy-batch6"
```

**Terminal B** on Linux:
```bash
python3 local-vm-labs/batch6_local_web_assessment.py assess --workspace "$HOME/academy-batch6"
```
For Windows substitute `py -3` and `"$HOME\academy-batch6"`.

**Expected baseline:** The server responds to `/health`, `/public` and `/private`. The first two work; the fictional private route mistakenly responds with HTTP 200. Four defensive response headers are absent. The checker should report **2/7 passing**. The private route contains only fake data; this intentionally weak local fixture must never be used on an outside network.

**What commands do:** `init` creates an unused disposable folder; `serve` starts the real local HTTP service; `assess` sends actual loopback GET requests and checks HTTP status, body and headers. Unlike a web UI simulation, these HTTP calls actually execute on your machine.

**Record evidence:** For each endpoint, note HTTP status, body and security response headers. Explain why receiving HTTP 200 is not proof of authorization. Explain why having a Content-Security-Policy header is only one layer of browser-side protection, not a replacement for server-side checks.

**Repair** (terminal B):
```bash
python3 local-vm-labs/batch6_local_web_assessment.py harden --workspace "$HOME/academy-batch6"
python3 local-vm-labs/batch6_local_web_assessment.py assess --workspace "$HOME/academy-batch6"
```

**Expected after repair:** HTTP 403 for the fake private route, and four configured response headers on the public response. All **7/7** checks should be true. This tests predefined behavior, not comprehensive production application security.

**Troubleshooting:** If `init` refuses the path, it already exists—do not overwrite it. If port 18766 is occupied by your own process, use the same unused `--port 18767` on both `serve` and `assess`. If the HTTP requests fail, verify terminal A is running; connection refused is different from a server returning HTTP 503. If `assess` reports malformed config, inspect *only the disposable training folder*. Never disable firewall/antivirus just to pass.

**Independent task:** Reset the fixture with `reset` and have an authorized partner select the next state without telling you. Capture evidence first, propose a remediation, apply `harden`, and verify. Do not claim this to be a secure blind exam: the local config is readable.

## Lab 2 — Network evidence analysis without traffic generation (35–50 minutes)

Use the built-in fictional event records. There is **no packet capture or network target**.

```bash
python3 local-vm-labs/batch6_security_triage.py evidence
python3 local-vm-labs/batch6_security_triage.py check --denied 2 --timeout 1 --highest WEB-01
```

**Expected:** five events total: 2 allow, 2 deny, 1 timeout. Sources are documentation addresses (`192.0.2.0/24`) and destinations are documentation addresses (`198.51.100.0/24`). The sample check earns **3/3**; it is provided to teach the output format. For an independent attempt, calculate counts and priorities before reading the answer.

**Explain:** Two denied connections are not two intrusions. A DNS timeout is a symptom and can be caused by multiple layers. Determine which additional authorized logs or time sources you would request.

**Troubleshooting:** If the Python module cannot be found, run from the cloned repository root. If the exact source output differs, use the current code as the evidence source and record the version/commit. Do not manufacture observations.

## Lab 3 — Vulnerability triage and business impact (40–60 minutes)

```bash
python3 local-vm-labs/batch6_security_triage.py prioritize
python3 local-vm-labs/batch6_security_triage.py report
```

**Expected priority:** WEB-01 first (likelihood 3 × impact 3 = teaching score 9). WEB-02 and NET-01 are lower. This score is **not CVSS or EPSS** and is not a validated likelihood of exploitation.

**Independent task:** Draft a fictional security advisory with asset, observed condition, reproducible steps performed in the owned lab, affected boundary, potential impact, severity assumptions, remediation owner, rollback and *retest evidence*. Distinguish a verified local behavior from a hypothetical production vulnerability.

## Lab 4 — Windows and Linux security tooling: observation and scope (30–45 minutes)

Run only on your machine, while the owned localhost server is active.

Windows PowerShell:
```powershell
Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -eq 18766 } | Select-Object LocalAddress,LocalPort,OwningProcess
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name,Id,CPU
```

Linux / Ubuntu / WSL:
```bash
ss -ltn '( sport = :18766 )'
ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6
```

**Expected:** a listener on `127.0.0.1:18766` while the lab server is running (availability and tools vary). A process table does not prove whether a web endpoint correctly enforces authorization. Avoid sharing personal process details.

**Independent task:** Explain why loopback binding prevents ordinary external network access, why this is not an impenetrable security boundary on a compromised host, and why the verified private-route behavior is stronger evidence than a generic open-port claim.

## Lab 5 — Professional findings packet (60 minutes)

Submit a local, redacted report with: scope and authorization, environment and version, timestamps, exact commands, baseline observations, interpretation, alternative hypothesis, remediation, retest observations, residual limitations, and recommendations. No raw passwords, genuine user identities, or other people's IP addresses.

**Objective evidence checkpoints:** web fixture 7/7 and offline network reasoning 3/3 are available for practice; they do not automatically evaluate the written report. Separate human rubric (5 × 20 points): scope, reproducibility, technical explanation, risk reasoning, repair/verification. Passing a fixture is not an independent professional competency review.

### Cleanup and safety

Stop the local server using Ctrl+C. The scripts only write to your explicitly designated disposable folder; they never delete files. Review the folder contents before manually removing them. Do not bridge the deliberately weak baseline fixture to outside networks.

### Known limitations

The private endpoint uses a *modeled authorization rule* and fictional data; no real login or user-permission system is present. The site is plaintext HTTP over loopback. The header checks verify fixed strings, not browser exploitation resistance. The network records are fictional, not collected packets. Actual vulnerability scanning of external assets is intentionally excluded. Windows and Linux CI tests validate the training software where available but cannot certify the learner's performance.
