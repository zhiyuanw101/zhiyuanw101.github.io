#!/usr/bin/env python3
"""Local staging server: rebuilds the site when a source file changes and reloads open pages.

Usage:  python3 tools/serve.py [port]        # default port 8765, then open http://localhost:8765

Watches content/, static/ and tools/. Each change runs tools/build.py in dev mode (BLOG_DEV=1),
which adds a small script to every page. The script polls /__build_status.json, reloads the page
after a successful rebuild, and shows a banner with the error after a failed one (the previous
build stays in public/). Nothing is published: publishing is a push to master (see AGENTS.md).
"""

import functools
import http.server
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
WATCH = [ROOT / "content", ROOT / "static", ROOT / "tools"]
STATUS = "__build_status.json"


def snapshot():
	return {
		p: p.stat().st_mtime
		for d in WATCH
		for p in d.rglob("*")
		if p.is_file() and "__pycache__" not in p.parts
	}


def build():
	started = time.strftime("%H:%M:%S")
	result = subprocess.run(
		[sys.executable, str(ROOT / "tools" / "build.py")],
		env={**os.environ, "BLOG_DEV": "1"},
		capture_output=True,
		text=True,
	)
	error = None if result.returncode == 0 else (result.stderr or result.stdout).strip()
	PUBLIC.mkdir(exist_ok=True)
	(PUBLIC / STATUS).write_text(json.dumps({"id": time.time(), "error": error}))
	print(f"[{started}] " + ("rebuilt" if error is None else "build FAILED:\n" + error), flush=True)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
	def log_message(self, *args):
		pass

	def end_headers(self):
		self.send_header("Cache-Control", "no-store")
		super().end_headers()


def main():
	port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
	build()
	handler = functools.partial(QuietHandler, directory=str(PUBLIC))
	server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
	threading.Thread(target=server.serve_forever, daemon=True).start()
	print(f"Staging at http://localhost:{port}  (watching content/, static/, tools/; Ctrl+C to stop)", flush=True)
	seen = snapshot()
	try:
		while True:
			time.sleep(0.5)
			now = snapshot()
			if now != seen:
				time.sleep(0.2)  # let editors finish writing
				seen = snapshot()
				build()
	except KeyboardInterrupt:
		server.shutdown()


if __name__ == "__main__":
	main()
