#!/usr/bin/env python3
"""Investigator VM's loopback-only multi-stage lab workspace.

Run in the investigator VM at 10.40.0.20/24 with target at 10.40.0.80/24.
Browser access ONLY inside investigator VM: http://127.0.0.1:8770.
Never forward this port, bridge guest NICs, or publish this service online.
No general-purpose shell, scans, dynamic URLs, or CORS.
"""
from __future__ import annotations
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json
import secrets

import three_room_client as lab

HOST = "127.0.0.1"
PORT = 8770
ORIGIN = f"http://{HOST}:{PORT}"
TOKEN = secrets.token_urlsafe(32)
REPORT = Path.home() / "academy-three-room-report.json"
MAX_BODY = 18000
MIN_WORDS = 45
STAGES = ("scope", "observe", "analyze", "retest", "report")
ROOMS = tuple(lab.CASES)


def report_default():
    return {"schema": "academy-investigator-workspace-v1", "scope_confirmed": False,
            "analysis": {room: "" for room in ROOMS}, "remediation": "",
            "history": [], "submitted": False}


def load_report():
    if REPORT.exists():
        if REPORT.is_symlink() or not REPORT.is_file():
            raise ValueError("Unsafe report path")
        doc = json.loads(REPORT.read_text(encoding="utf-8"))
        if doc.get("schema") != "academy-investigator-workspace-v1":
            raise ValueError("Unknown report schema")
        return doc
    return report_default()


def save_report(data):
    if REPORT.is_symlink() or (REPORT.exists() and not REPORT.is_file()):
        raise ValueError("Unsafe report path")
    REPORT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def quality_gate(data):
    return (all(len(str(data.get("analysis", {}).get(r, "")).split()) >= MIN_WORDS for r in ROOMS)
            and len(str(data.get("remediation", "")).split()) >= MIN_WORDS)


def stage_status():
    report = load_report()
    evidence = lab.read()
    phases = evidence.get("captures", {})
    before = phases.get("vulnerable")
    after = phases.get("patched")
    grade = lab.grade_score()
    return {
        "report": report, "has_vulnerable_capture": bool(before),
        "has_patched_capture": bool(after),
        "captured_modes": list(phases),
        "scoring": grade,
        "writing_requirements": {r: len(report["analysis"].get(r, "").split()) for r in ROOMS},
        "remediation_words": len(report.get("remediation", "").split()),
        "minimum_words_each": MIN_WORDS,
        "writing_length_gate": quality_gate(report),
        "candidate_ready": bool(before and after and report["scope_confirmed"]
                                and grade["score"] == 100 and quality_gate(report)),
        "limitations": "Local evidence can be edited. Written work is not fact-graded. No identity attestation.",
    }


def api_action(payload):
    action = payload.get("action")
    if not isinstance(action, str):
        raise ValueError("Action required")
    report = load_report()
    if action == "status":
        return stage_status()
    if report["submitted"] and action not in ("status", "grade"):
        raise ValueError("This attempt is locked after submission")
    if action == "scope":
        if payload.get("confirmed") is not True:
            raise ValueError("Confirm isolated internal network and authorized ownership first")
        # A learner acknowledgement does not verify the hypervisor configuration.
        report["scope_confirmed"] = True
        report["history"].append("Learner affirmed lab scope at " + datetime.now(timezone.utc).isoformat())
        save_report(report)
        return stage_status()
    if not report.get("scope_confirmed"):
        raise ValueError("Confirm the isolated lab scope before running actions")
    if action == "capture-vulnerable":
        lab.capture("vulnerable")
        report["history"].append("Vulnerable-phase evidence captured")
        save_report(report)
        return stage_status()
    if action == "analysis":
        if not stage_status()["has_vulnerable_capture"]:
            raise ValueError("Capture vulnerable responses before analysis")
        room = payload.get("room")
        content = payload.get("text")
        if room not in ROOMS or not isinstance(content, str) or len(content) > 7500:
            raise ValueError("Invalid analysis room or text")
        report["analysis"][room] = content
        save_report(report)
        return stage_status()
    if action == "capture-patched":
        if not stage_status()["has_vulnerable_capture"]:
            raise ValueError("Capture vulnerable mode first")
        if not all(len(report["analysis"].get(room, "").split()) >= MIN_WORDS for room in ROOMS):
            raise ValueError("Write at least 45 words for each observed finding before patched retest")
        lab.capture("patched")
        report["history"].append("Patched-phase evidence captured")
        save_report(report)
        return stage_status()
    if action == "remediation":
        content = payload.get("text")
        if not isinstance(content, str) or len(content) > 7500:
            raise ValueError("Invalid remediation text")
        report["remediation"] = content
        save_report(report)
        return stage_status()
    if action == "grade":
        return stage_status()
    if action == "submit":
        status = stage_status()
        if not status["candidate_ready"]:
            raise ValueError("Scope, captures, objective checks and written report requirements are incomplete")
        report["submitted"] = True
        report["submitted_utc"] = datetime.now(timezone.utc).isoformat()
        save_report(report)
        return stage_status()
    raise ValueError("Unsupported workspace action")


HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer"><title>Academy — Private Investigator Workspace</title>
<style>
:root{color-scheme:dark;background:#101c23;color:#f2eee4;font:15px/1.55 system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0}header{padding:15px 20px;background:#1d3038;border-bottom:1px solid #5c737b}
h1{font-size:clamp(22px,3.2vw,30px)}h2{font-size:18px}h3{font-size:16px;color:#e8cb91}
main{max-width:1450px;margin:auto;padding:15px;display:grid;grid-template-columns:minmax(330px,.85fr) minmax(380px,1.15fr);gap:14px}
section{min-width:0;background:#21343b;border:1px solid #546c75;border-radius:13px;padding:17px;margin-bottom:14px}
button{background:#e5c993;color:#14262d;border:0;border-radius:9px;min-height:43px;padding:10px 14px;font-weight:740;cursor:pointer}
button:disabled{opacity:.5;cursor:not-allowed}textarea{width:100%;min-height:125px;background:#0d2129;color:white;border:1px solid #899da6;border-radius:9px;padding:11px;font:inherit}
pre{background:#0c1b22;border:1px solid #647983;border-radius:10px;max-height:430px;overflow:auto;padding:13px;white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.55 ui-monospace,monospace}
label{display:block;margin:11px 0 6px;font-weight:700}.muted,small{color:#c3cecf}.step{border-top:1px solid #526b74;padding:13px 0}.state{color:#efce95}.tools{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}select{background:#132832;color:white;padding:10px;border:1px solid #8095a0;border-radius:8px}
@media(max-width:900px){main{grid-template-columns:1fr;padding:10px}}
</style></head><body><header><strong>ETHICAL HACKING ACADEMY · LOCAL INVESTIGATOR WORKSPACE</strong><p>Inside investigator VM only · 127.0.0.1:8770 · No arbitrary terminal or remote access</p></header>
<main><div><section><h1>Multi-stage web investigation</h1>
<p>Investigate three synthetic access-control defects on your separate authorized target VM, document evidence, retest after patching, and receive objective HTTP evidence grading.</p>
<p class="muted">A scope acknowledgement is not a real network safety verification. Confirm your investigator is 10.40.0.20, target 10.40.0.80, internal switch only, and neither guest has a default route.</p>
<div class="step"><h3>1 · Authorized scope</h3><button id="scope">Confirm private lab configuration</button></div>
<div class="step"><h3>2 · Vulnerable-state evidence</h3><button id="before">Capture three vulnerabilities</button></div>
<div class="step"><h3>3 · Analysis of each finding</h3><label for="room">Room</label>
<select id="room"><option value="ownership">Object ownership</option><option value="export">Report export</option><option value="debug">Debug exposure</option></select>
<textarea id="analysis" placeholder="Explain observation, expected policy, missing check, risk, supporting HTTP status and evidence limitations."></textarea>
<div class="tools"><button id="save-analysis">Save room analysis</button><span class="state" id="analysis-words"></span></div></div>
<div class="step"><h3>4 · Patch and retest</h3><p>Stop the separate target server with Ctrl+C and restart it using <code>python3 three_room_target.py --patched</code> inside the target VM. Then capture the corrected HTTP responses here.</p><button id="after">Capture patched results</button></div>
<div class="step"><h3>5 · Remediation and sign-off</h3><textarea id="remediation" placeholder="Explain fixes, regression checks, residual risks, rollback strategy, and limits of this synthetic authentication model."></textarea>
<div class="tools"><button id="save-remediation">Save remediation</button><button id="grade">Calculate grade</button><button id="submit">Lock and submit attempt</button></div>
</div><p id="notice" class="state" role="status"></p></section></div>
<div><section><h2>Live local evidence</h2><p class="muted">Collected on the investigator VM through fixed HTTP endpoints on your target. No network scan or arbitrary URL execution.</p><pre id="evidence">Select a stage to start.</pre><h2>Current assessment</h2><pre id="results">No evidence yet.</pre></section>
<section><h2>Evidence provenance</h2><p class="muted">Recorded results and report live on this VM in JSON files. Evidence can be edited locally and is not independently authenticated. Word-count gates do not evaluate reasoning accuracy. A qualified assessor must observe real practice.</p>
<p class="muted">The browser only connects to a loopback server on the investigator VM, which in turn makes predefined requests to 10.40.0.80:8767. Public GitHub Pages cannot connect directly to this workspace.</p></section></div></main>
<script>
'use strict';const token=__TOKEN__,E=id=>document.getElementById(id);let current={};
function view(d){current=d;const r=d.report||{};E('evidence').textContent=JSON.stringify({captured_modes:d.captured_modes,history:r.history,scope_confirmed:r.scope_confirmed},null,2);
E('results').textContent=JSON.stringify({score:d.scoring?.score||0,maximum:100,has_vulnerable_capture:d.has_vulnerable_capture,has_patched_capture:d.has_patched_capture,writing_requirements:d.writing_requirements,remediation_words:d.remediation_words,candidate_ready:d.candidate_ready,submitted:r.submitted},null,2);
E('remediation').value=r.remediation||'';E('remediation').disabled=!!r.submitted;E('analysis').disabled=!!r.submitted;
E('submit').disabled=!!r.submitted;E('before').disabled=!!r.submitted;E('after').disabled=!!r.submitted;E('scope').disabled=!!r.submitted;E('save-analysis').disabled=!!r.submitted;E('save-remediation').disabled=!!r.submitted;
showRoom();}
function showRoom(){E('analysis').value=current.report?.analysis?.[E('room').value]||'';E('analysis-words').textContent=E('analysis').value.trim().split(/\s+/).filter(Boolean).length+' / 45 words';}
async function api(action,body={}){E('notice').textContent='Checking local lab…';try{
const response=await fetch('/api/workspace',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json','X-Workspace-Token':token},body:JSON.stringify({action,...body})});
const data=await response.json();if(!response.ok){E('notice').textContent=data.error||'Local action failed';return}
view(data);E('notice').textContent='Local lab state updated.';
}catch(e){E('notice').textContent='Local server unavailable: '+e.message}}
E('room').onchange=showRoom;E('analysis').oninput=()=>E('analysis-words').textContent=E('analysis').value.trim().split(/\s+/).filter(Boolean).length+' / 45 words';
E('scope').onclick=()=>{if(confirm('Have you checked both VM network adapters, private addresses and absence of default routes?'))api('scope',{confirmed:true})};
E('before').onclick=()=>api('capture-vulnerable');
E('save-analysis').onclick=()=>api('analysis',{room:E('room').value,text:E('analysis').value});
E('after').onclick=()=>api('capture-patched');
E('save-remediation').onclick=()=>api('remediation',{text:E('remediation').value});
E('grade').onclick=()=>api('grade');
E('submit').onclick=()=>{if(confirm('Lock this local practice submission?'))api('submit')};
api('status');
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def send(self, code, obj, json_output=True):
        data = (json.dumps(obj).encode("utf-8") if json_output else obj)
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8" if json_output else "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; form-action 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def allowed_host(self):
        return self.headers.get("Host") == f"{HOST}:{PORT}"

    def do_GET(self):
        if not self.allowed_host():
            return self.send(403, {"error": "Unexpected Host"})
        if urlsplit(self.path).path != "/":
            return self.send(404, {"error": "Not found"})
        self.send(200, HTML.replace("__TOKEN__", json.dumps(TOKEN)).encode("utf-8"), False)

    def do_POST(self):
        if not self.allowed_host() or self.headers.get("Origin") != ORIGIN or self.headers.get("X-Workspace-Token") != TOKEN:
            return self.send(403, {"error": "Host, Origin or token rejected"})
        if urlsplit(self.path).path != "/api/workspace":
            return self.send(404, {"error": "Not found"})
        if self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
            return self.send(415, {"error": "JSON required"})
        try:
            n = int(self.headers.get("Content-Length", "-1"))
            if n < 1 or n > MAX_BODY:
                return self.send(413, {"error": "Invalid body length"})
            body = json.loads(self.rfile.read(n))
            if not isinstance(body, dict):
                raise ValueError("Expected JSON object")
            return self.send(200, api_action(body))
        except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
            return self.send(400, {"error": str(exc)})

    def log_message(self, fmt, *args):
        return


if __name__ == "__main__":
    print(f"LOCAL multi-stage investigator workspace: {ORIGIN}")
    print("Open in the investigator VM's browser; never forward port 8770.")
    try:
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("Stopped.")
