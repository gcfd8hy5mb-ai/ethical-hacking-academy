#!/usr/bin/env python3
"""Loopback-only browser console for the Ethical Hacking Academy offline Linux lab.

Run as a normal user INSIDE your own Linux VM. No general-purpose shell,
remote listeners, arbitrary filesystem paths, process execution, or CORS.
"""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json
import os
import secrets
import stat

from academy_lab import BASE, files, check_state, setup

HOST = "127.0.0.1"
PORT = 8765
ORIGIN = f"http://{HOST}:{PORT}"
TOKEN = secrets.token_urlsafe(32)
MAX_BODY = 9000

HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>Academy · Real Local Linux Lab</title><style>
:root{color-scheme:dark;background:#111d24;color:#f3efe6;font:16px/1.5 system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0}header{padding:14px 20px;background:#1d3039;border-bottom:1px solid #65747b}
header a{color:#e7c78d}main{max-width:1350px;margin:auto;padding:16px;display:grid;gap:16px;grid-template-columns:1fr 1fr}
section{background:#23343c;border:1px solid #5e717b;border-radius:13px;padding:19px;min-width:0}
h1{font-size:clamp(22px,3vw,31px);margin:7px 0}h2{font-size:19px}
small,p{color:#d0d9d9}button{background:#e4c991;color:#17252c;border:0;padding:10px 13px;border-radius:8px;min-height:44px;font-weight:750;cursor:pointer}
button:disabled{opacity:.5}textarea{width:100%;min-height:175px;background:#0b1a21;color:white;border:1px solid #8ba0a5;border-radius:9px;padding:12px;font:15px/1.5 ui-monospace,monospace}
pre{background:#0c1b22;border:1px solid #566b75;min-height:240px;max-height:510px;overflow:auto;padding:14px;white-space:pre-wrap;overflow-wrap:anywhere;border-radius:9px;font:13px/1.55 ui-monospace,monospace}
.buttons{display:flex;gap:8px;flex-wrap:wrap}.notice{color:#e4ca95}
@media(max-width:850px){main{grid-template-columns:1fr;padding:10px}section{padding:14px}}
</style></head><body><header><strong>ETHICAL HACKING ACADEMY · REAL LOCAL LINUX LAB</strong>
<p>Bound only to 127.0.0.1 inside your Linux virtual machine. Not a remote console or arbitrary shell.</p></header>
<main><section><h1>Hands-on filesystem classroom</h1><p>These tasks operate on <code>~/academy-local-lab</code> using real Python/Linux filesystem operations inside your VM. Start with setup, inspect the evidence, perform fixes, and validate.</p>
<div class="buttons">
<button data-action="setup">Create training files</button>
<button data-action="environment">Lab status</button>
<button data-action="permissions">Inspect permissions</button>
<button data-action="logs">Read DNS log</button>
<button data-action="config">Inspect config</button>
</div>
<h2>Approved corrections</h2>
<div class="buttons">
<button data-action="fix-permissions">Set mode 640</button>
<button data-action="fix-config">Repair listen directive</button>
<button data-action="check">Validate tasks</button>
<button data-action="export">Export evidence</button>
</div>
<h2>Incident interpretation</h2>
<p>Write what the DNS timeout means, what it cannot prove, and how you would safely investigate further. Text content is checked for basic completeness only.</p>
<textarea id="finding" placeholder="Describe the DNS timeout, relevant log evidence, limits of attribution and authorized follow-up checks."></textarea>
<div class="buttons"><button id="save-finding">Save investigation finding</button></div>
<p id="feedback" class="notice" role="status"></p>
<p><small>Only the approved training files can be changed. No root permissions, no shell execution, no remote device control, no production network or VM provisioning. No result automatically syncs to your Academy login.</small></p>
</section><section><h2>Local lab output</h2>
<pre id="output" role="log" aria-live="polite">Select Lab status, or Create training files if this is your first run.</pre>
<p><small>Tip: open the VM's regular Terminal for unrestricted Linux practice within your authorized, isolated guest. This browser interface deliberately provides a small allowlisted set of training operations.</small></p></section></main>
<script>
const token=__TOKEN__,out=document.getElementById('output'),feedback=document.getElementById('feedback');
async function act(action,extra={}){
feedback.textContent='Running local lab action…';
try{const r=await fetch('/api/action',{method:'POST',credentials:'same-origin',
headers:{'Content-Type':'application/json','X-Lab-Token':token},
body:JSON.stringify({action,...extra})});
const body=await r.json();out.textContent=body.output||body.error||'No output';
feedback.textContent=r.ok?'Local action completed.':'Local action failed ('+r.status+').';
}catch(e){feedback.textContent='Cannot connect to local VM lab server: '+e.message}
}
document.querySelectorAll('[data-action]').forEach(b=>b.addEventListener('click',()=>act(b.dataset.action)));
document.getElementById('save-finding').onclick=()=>act('save-finding',{text:document.getElementById('finding').value});
</script></body></html>"""


def safe_file(path: Path) -> Path:
    """Reject symlinks and unexpected file types anywhere in this training tree."""
    if not BASE.is_dir() or BASE.is_symlink():
        raise ValueError("Training folder absent or unsafe: run setup on an empty lab.")
    try:
        rel = path.relative_to(BASE)
    except ValueError as exc:
        raise ValueError("Path outside the lab is denied") from exc
    current = BASE
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Symlinks are not permitted in training paths")
    if path.exists() and not path.is_file():
        raise ValueError("Expected a regular training file")
    return path


def action(name: str, payload: dict) -> str:
    if name == "setup":
        setup()  # refuses to overwrite an existing directory
        return "Created a local training folder. Select Lab status next."
    f = files()
    if not BASE.is_dir() or BASE.is_symlink():
        return "Lab missing. Click Create training files first."
    if name == "environment":
        return f"Training root: {BASE}\nFile-state checks: {json.dumps(check_state(), indent=2)}"
    if name == "permissions":
        p = safe_file(f["permissions"])
        return f"{p}: mode {stat.S_IMODE(p.stat().st_mode):04o}; owner UID {p.stat().st_uid}; group GID {p.stat().st_gid}"
    if name == "logs":
        return safe_file(f["logs"]).read_text(encoding="utf-8", errors="replace")[:6000]
    if name == "config":
        return safe_file(f["config"]).read_text(encoding="utf-8", errors="replace")[:6000]
    if name == "fix-permissions":
        p = safe_file(f["permissions"])
        os.chmod(p, 0o640, follow_symlinks=False)
        return "Real VM filesystem permission changed to 0640. Re-inspect, then validate."
    if name == "fix-config":
        p = safe_file(f["config"])
        before = p.read_text(encoding="utf-8", errors="replace")
        if "listen 80 extra;" not in before:
            return "Training directive not present; no file changed."
        p.write_text(before.replace("listen 80 extra;", "listen 80;"), encoding="utf-8")
        return "Real VM training configuration file corrected. This does not start nginx."
    if name == "save-finding":
        text = payload.get("text", "")
        if not isinstance(text, str) or len(text) > 5000:
            raise ValueError("Finding must be plain text under 5001 characters")
        safe_file(f["finding"]).write_text(text, encoding="utf-8")
        return "Finding saved in your VM training folder."
    if name == "check":
        results = check_state()
        result = json.dumps(results, indent=2)
        if all(results.values()):
            result += "\nTRAIN{OFFLINE_LINUX_MISSIONS_COMPLETE}\nNote: written analysis remains ungraded."
        return result
    if name == "export":
        results = check_state()
        p = safe_file(f["evidence"])
        p.write_text(json.dumps({"schema": "academy-local-console-v1", "checks": results,
            "limitation": "Self-generated lab file checks, not independent practical assessment."}, indent=2) + "\n",
            encoding="utf-8")
        return f"Evidence JSON saved inside the VM: {p}"
    raise ValueError("Unknown or disallowed lab action")


class Handler(BaseHTTPRequestHandler):
    def _headers(self, code: int, mime: str, size: int) -> None:
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(size))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
        self.end_headers()

    def _reply(self, code: int, value: dict) -> None:
        data = json.dumps(value).encode("utf-8")
        self._headers(code, "application/json; charset=utf-8", len(data))
        self.wfile.write(data)

    def _allowed_host(self) -> bool:
        return self.headers.get("Host") == f"{HOST}:{PORT}"

    def do_GET(self) -> None:
        if not self._allowed_host():
            self._reply(403, {"error": "Host rejected"})
            return
        if urlsplit(self.path).path != "/":
            self._reply(404, {"error": "Not found"})
            return
        html = HTML.replace("__TOKEN__", json.dumps(TOKEN)).encode("utf-8")
        self._headers(200, "text/html; charset=utf-8", len(html))
        self.wfile.write(html)

    def do_POST(self) -> None:
        if not self._allowed_host() or self.headers.get("Origin") != ORIGIN or self.headers.get("X-Lab-Token") != TOKEN:
            self._reply(403, {"error": "Origin, host or authorization check failed"})
            return
        if urlsplit(self.path).path != "/api/action":
            self._reply(404, {"error": "Not found"})
            return
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            self._reply(415, {"error": "JSON required"})
            return
        try:
            size = int(self.headers.get("Content-Length", "-1"))
            if size < 1 or size > MAX_BODY:
                self._reply(413, {"error": "Invalid request size"})
                return
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict) or not isinstance(payload.get("action"), str):
                raise ValueError("Invalid action request")
            text = action(payload["action"], payload)
            self._reply(200, {"output": text})
        except (ValueError, OSError, KeyError, UnicodeError) as exc:
            self._reply(400, {"error": str(exc)})

    def log_message(self, fmt: str, *args: object) -> None:
        return


if __name__ == "__main__":
    print("Local VM lab console (allowlisted operations only).")
    print("Open a browser INSIDE THE SAME VM at " + ORIGIN)
    print("Press Ctrl+C to stop. Never port-forward this service.")
    try:
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nLab console stopped.")
