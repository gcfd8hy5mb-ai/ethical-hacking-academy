# Batch 3 — Real-computer labs (Windows, Linux, Python, local troubleshooting)

These labs run on **your own computer** or a virtual machine you are authorized to use.
They are deliberately offline or read-only. Do not target other devices, roommates'
computers, public services, or business systems without explicit authorization.

## Setup and limitations

* Windows 10/11: open **PowerShell**. Install Python 3 if needed; check with `py -3 --version`.
* Ubuntu/Linux/WSL: open a **terminal**. Check `python3 --version`.
* Download/clone the Academy repository using the GitHub link or ZIP. Run commands
  from the repository root; do not paste commands from untrusted pages.
* A smartphone can read the instructions but cannot execute Windows or Linux OS commands.
* Save screenshots and answer notes in your own folder; the Academy does not upload
  those files or certify independent mastery.
* No administrative privileges, packet scanning, exploitation or network services
  are required. Expected outputs differ by OS version and machine.

## Lab 1: Safe file-evidence workstation (40–60 minutes)

**Goal:** create only disposable fictional files, verify content and permission
state, analyze synthetic sign-ins, and explain the limits of a passing automated check.

**Windows PowerShell:**
```powershell
py -3 --version
py -3 local-vm-labs/batch3_offline_lab.py init --workspace "$HOME\academy-batch3-lab"
py -3 local-vm-labs/batch3_offline_lab.py check --workspace "$HOME\academy-batch3-lab" --json
Get-FileHash "$HOME\academy-batch3-lab\events.csv" -Algorithm SHA256
Get-Acl "$HOME\academy-batch3-lab\permissions\private.txt" | Format-List
```

**Ubuntu / WSL / Linux:**
```bash
python3 --version
python3 local-vm-labs/batch3_offline_lab.py init --workspace "$HOME/academy-batch3-lab"
python3 local-vm-labs/batch3_offline_lab.py check --workspace "$HOME/academy-batch3-lab" --json
sha256sum "$HOME/academy-batch3-lab/events.csv"
ls -l "$HOME/academy-batch3-lab/permissions/private.txt"
```

**Expected:** four synthetic records (two success, two fail); a report with
`"synthetic_event_counts": true` and `"loopback_only": true`.
On Linux `private.txt` should show owner-only mode `-rw-------`, subject
to filesystem semantics. On Windows a `null` POSIX-mode result is expected:
review the displayed ACL rather than assuming it is private. `Get-FileHash`
and `sha256sum` each produce a SHA-256 digest, but the output format differs.
Hashing demonstrates file-content consistency, not acquisition chain of custody.

**Troubleshooting:** if `init` refuses the workspace, it already exists:
do NOT overwrite it. Choose a new name such as `academy-batch3-lab-2`.
If Python is missing, install a trusted Python 3 build or use the written
paper exercises. If a permission check fails, inspect the owning filesystem;
do not apply `sudo`, `chmod -R`, or broad permissions to make it pass.

**Assessment:** Explain (1) why two failures do not prove intrusion,
(2) what each SHA-256 digest establishes, (3) why `127.0.0.1` limits a
hypothetical service to loopback, and (4) why a fixture passing is not
evidence that real enterprise systems are secure.

## Lab 2: Windows observational triage (30–45 minutes)

Run these **read-only commands** in a normal, non-administrator PowerShell:
```powershell
Get-ComputerInfo | Select-Object WindowsProductName,OsVersion
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name,Id,CPU
Get-Service | Select-Object -First 10 Name,Status,StartType
Get-NetIPConfiguration | Select-Object InterfaceAlias,IPv4Address,IPv4DefaultGateway,DNSServer
```

**Expected:** operating system details, top five processes sorted by
*cumulative CPU seconds*, a service-state sample, and the local interface
configuration. Empty gateway entries may be normal for disconnected adapters.
A stopped service alone does not prove a fault. Record process names without
sharing private user information.

**Troubleshooting:** `Get-NetIPConfiguration` is Windows-specific; this
lab is not for Linux shells. A command absent on an older version can be
replaced by the graphical Task Manager and Settings → Network. A command
error should become part of your evidence, not a reason to elevate privileges.

**Assessment:** Compare cumulative CPU time with live CPU %, identify one
benign reason for a stopped service, and explain which configuration detail
could be relevant to a DNS issue without changing the settings.

## Lab 3: Linux file, service and route interpretation (30–45 minutes)

In an Ubuntu VM or WSL distribution:
```bash
whoami
pwd
ls -ld "$HOME/academy-batch3-lab"
ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6
ip route show
```

**Expected:** your effective user, current directory, lab directory mode,
a snapshot of up to five busiest processes and routing entries. In WSL some
platform interfaces may be presented differently. An empty route table or
missing `ip` utility is a diagnostic fact, not permission to change networking.

**Assessment:** Differentiate effective identity from process owner, explain
why snapshot CPU% can differ from cumulative CPU counters, and identify a
default route *if one is present*. Do not test arbitrary remote IP addresses.

## Lab 4: Python evidence reasoning (30–60 minutes)

Run the code below in a local Python 3 interactive session or a disposable
script. It reads **only** the synthetic file you created:
```python
from pathlib import Path
from collections import Counter
import csv

path = Path.home() / "academy-batch3-lab" / "events.csv"
with path.open(newline="", encoding="utf-8") as stream:
    events = list(csv.DictReader(stream))
print(Counter(row["result"] for row in events))
print(sorted({row["user"] for row in events if row["result"] == "fail"}))
```

**Expected:** `Counter({'success': 2, 'fail': 2})` (order can vary),
then `['blair']`. If you used another workspace name, update the path
accordingly. The program produces counts and categories, not proof of a breach.

**Challenge:** Make a *separate* copy of `events.csv` in your disposable
workspace and add one failed record for fictional `alex`. Predict the counts
before executing, then explain the change. Never edit genuine sign-in logs.

## Independent evidence sheet — 100-point self-review

Use one page per exercise. Record date, computer OS, consent/ownership,
exact commands, predicted output, observed output (redacted), explanation,
one alternative hypothesis, troubleshooting and a safe next step.

Scoring is **self-review only**: accurate command/method explanation (20),
expected-versus-observed interpretation (20), evidence and reproducibility (20),
alternative hypothesis and limitations (20), authorized scope and cleanup (20).
Aim for 80+ before progressing, but that threshold is not an independent exam.

**Cleanup:** Retain the lab folder for review or remove it manually only after
confirming it contains exclusively the disposable artifacts you generated.
The Academy scripts never remove or overwrite your existing folders.
