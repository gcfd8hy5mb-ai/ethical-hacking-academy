# Batch 4 — VM setup, administration and independent network fault isolation

**Environment:** only your own Windows 10/11 computer, Linux machine, or VM you are explicitly authorized to administer. This batch is a guided practical **extension**, not proof of certification or professional readiness. Use written evidence sheets; no student completion keys change.

## 1 — Prepare a disposable VM (45–90 minutes)

On a Windows host, confirm available RAM and CPU virtualization using Task Manager → Performance → CPU. Open Windows Features to confirm your permitted virtualization platform, if installed. On Linux hosts, inspect system memory with `free -h` and virtualization flags with `lscpu` (available values vary). Choose a reputable hypervisor supported by your computer. Do not disable host security controls or download prebuilt hacking distributions from unknown sites.

For a beginner Ubuntu VM:
1. Download an Ubuntu installation image from the official Ubuntu distribution website. Verify the published checksum where provided.
2. Create a VM named `academy-ubuntu-offline` with a small virtual disk, approximately **2 vCPUs, 2–4 GB RAM and 20–25 GB storage**, if the host has capacity. These are starting points, not compatibility guarantees; leave enough RAM for the host.
3. Use a disconnected or **host-only** virtual network while practicing the following diagnostics. Host-only network still may communicate with the host, so do not assume it is an impenetrable security boundary. Do not bridge a security lab VM into a shared network.
4. Install Linux, update through trusted channels when connectivity is explicitly enabled, then take a baseline snapshot if your hypervisor supports one.
5. Record VM hostname, version, RAM, storage, virtual network setting and snapshot identifier. Test shutdown and restore only with disposable practice data.

**Verification:** the guest boots, has a distinct user account and can display system information. A snapshot is not a substitute for backups.

**Troubleshooting:** if virtualization is missing, investigate host firmware support and policy before making changes. If VM memory is insufficient, reduce guest size or use WSL/another lightweight local lab. A Chromebook's supported virtualization varies by model and policy.

**Questions:** What separates the host from guest? Why is an isolated virtual network preferable for initial practice? What cannot a VM snapshot protect?

## 2 — Linux administration evidence (30–50 minutes)

Commands execute inside your **owned Linux VM**, as an unprivileged user:
```bash
id
uname -a
df -h "$HOME"
ps -eo pid,comm,%cpu --sort=-%cpu | head -n 8
ip -br address
ip route show
```
Expected: account and groups, kernel identification, space usage, process snapshot, interface addresses and routes. A disconnected VM may have no default route. The `ip` command might be absent from minimal systems. Do not install packages or modify routes just to produce a screenshot. Record timestamps and relevant lines.

Independent task: Explain which command tests identity, which reveals storage pressure, and which would distinguish absent route from absent DNS information. Do not confuse percentage CPU with cumulative CPU time.

## 3 — Windows administration evidence (30–50 minutes)

On your own Windows computer in **normal PowerShell**:
```powershell
Get-ComputerInfo | Select-Object WindowsProductName,OsVersion
Get-LocalUser | Select-Object Name,Enabled
Get-Service | Select-Object -First 10 Name,Status,StartType
Get-NetIPConfiguration | Select-Object InterfaceAlias,IPv4Address,IPv4DefaultGateway,DNSServer
```
Expected: OS version, local account metadata, service statuses and interface configuration. Some managed systems restrict a cmdlet; log the actual error and continue. **Do not include real account names or IP addresses** in a publicly shared report. Service Stopped does not prove compromise.

Independent task: Show a service status and name two distinct explanations. Explain what default gateway means and when an empty value is expected.

## 4 — Offline network-fault challenge (45–60 minutes)

Run from the repository directory; Python 3 standard library only.
```bash
python3 local-vm-labs/batch4_fault_isolation.py --list
python3 local-vm-labs/batch4_fault_isolation.py --case dns
python3 local-vm-labs/batch4_fault_isolation.py --case dns --answer A
```
On Windows, replace `python3` with `py -3`. Do **not** treat the sample answer `A` as an answer for every case. Read the evidence and select the next low-risk diagnostic action for **dns**, **route**, **service**, and **permissions**. The feedback explains the inference and its limits. No real packets, services, commands or remote devices are touched by this program.

Expected: four cases listed; each case prints fictional evidence and three alternatives. With `--answer`, the program reports correct/incorrect and the reason. `--json` with `--answer` gives machine-readable feedback.

**Troubleshooting:** If `python3` is unavailable, check your trusted Python installation or work through the case on paper. If a case ID is invalid, use `--list`. Results are read-only and aren't saved to the Academy exam record.

## 5 — Independent practical assessment rubric (100 points, self-reviewed)

For **each** of four scenarios, submit a local written report with: scope and setup, evidence table, command/method chosen, interpretation, competing hypotheses, decision and limitation. Five dimensions worth 20 points each: evidence accuracy; command/method understanding; competing-hypothesis reasoning; safe next action; reproducibility and documentation.

**Do not award full credit just for guessing an option.** Compare the learner's evidence narrative and machine screenshots with actual results. A reviewer must still assess independent competence separately. No official accreditation or real-world hacking authorization is implied.

Next escalation after this batch: a supervised sandbox with genuinely running local services, fixed/verified faults, and outside review of the student's diagnostic write-up.
