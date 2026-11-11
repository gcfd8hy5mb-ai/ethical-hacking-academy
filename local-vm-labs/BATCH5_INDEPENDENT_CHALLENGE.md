# Batch 5B — Independent live-service diagnostic challenge

**Prerequisites:** Python 3, downloaded Academy repository, owned Windows/Linux/macOS computer or authorized VM. No real network targets are needed. All HTTP requests and server connections are restricted to `127.0.0.1`.

## Setup: two terminals

In terminal A, from the repository root:

Linux / WSL:
```bash
python3 local-vm-labs/batch5_local_service.py init --workspace "$HOME/academy-batch5-exam"
python3 local-vm-labs/batch5_local_service.py serve --workspace "$HOME/academy-batch5-exam"
```

Windows PowerShell:
```powershell
py -3 local-vm-labs/batch5_local_service.py init --workspace "$HOME\academy-batch5-exam"
py -3 local-vm-labs/batch5_local_service.py serve --workspace "$HOME\academy-batch5-exam"
```

Leave the server running. Use terminal B for the challenge below. Substitute `py -3` and the Windows workspace for `python3` and the Linux workspace on Windows.

## Step 1 — Unknown fault assigned

```bash
python3 local-vm-labs/batch5_independent_challenge.py start --workspace "$HOME/academy-batch5-exam"
```

One of three controlled service modes is assigned: HTTP 503 unavailable, HTTP 403 record denial, or HTTP 200 incorrect record content. The command does not reveal the selected mode in normal output. This is a learning exercise, **not tamper-resistant**: the configuration and challenge file are visible on your own computer. For independent assessment, do not examine these files until after submitting the diagnosis.

## Step 2 — Observe, predict, and diagnose before modifying anything

```bash
python3 local-vm-labs/batch5_independent_challenge.py inspect --workspace "$HOME/academy-batch5-exam"
```

The command sends actual localhost HTTP requests to `/health` and `/records`. Record the HTTP status and body for both endpoints, one alternative explanation, and the difference between status and data correctness. If both endpoints return a connection error, confirm terminal A is still serving; this is not an HTTP 503.

Submit a diagnosis **once** using one of the exact labels `stopped`, `denied` or `bad-data`. Include at least 50 characters of technical evidence:

```bash
python3 local-vm-labs/batch5_independent_challenge.py diagnose --workspace "$HOME/academy-batch5-exam" --answer denied --evidence "Health returned HTTP 200, but records returned HTTP 403; the listener is available and the training app denies the records path."
```

The above answer is an **example only** and may be incorrect for your assigned fault. The diagnosis is recorded on your local disk before the explanation is shown. A correct first diagnosis earns **3 objective points**.

## Step 3 — Repair and verify independently

The training service reads only the disposable `service.json` configuration. After diagnosing, repair it safely:

```bash
python3 local-vm-labs/batch5_local_service.py fault --workspace "$HOME/academy-batch5-exam" --mode healthy
python3 local-vm-labs/batch5_independent_challenge.py grade --workspace "$HOME/academy-batch5-exam"
```

The grade command checks the *running server*, not just the config file. It awards up to **3 repair points**, one each for correct health response, accessible records, and exact expected records. Max machine-scored result: **6/6**. It does not award credit for reasoning quality, evidence authenticity, or safe troubleshooting procedures.

If the server is not running, verification cannot pass. If the port is occupied, stop the competing process only if it is yours or choose another nonprivileged port and pass the same `--port` to the server and `inspect`/`grade`.

## Step 4 — Human evaluation: 4 additional rubric points

Reviewer scores **0–1 each** for (1) correctly explaining evidence and limitations, (2) a reproducible command/timestamp record, (3) an alternate hypothesis and why it is weaker, and (4) authorized scope, safe repairs, and cleanup. The total assessment is **10 possible points**, but only 6 are machine scored. A student self-score is not an independent competency validation.

Record your results locally. There is **no** automatic sync to Academy lesson/exam progress. Use a new disposable workspace for another attempt. Stop the server with Ctrl+C in terminal A. Do not delete unrelated folders.

### Important limitations
- HTTP fault modes are *simulated application states*, though the underlying server and requests are real.
- The fault is not cryptographically hidden and local files can be inspected or edited; do not call it a secure blind exam.
- No remote hosts, user credential attacks, port scans, OS ACL changes, DNS reconfiguration or firewall disabling are required.
- A green automated score confirms a known fixture state only, not professional hands-on competence.
