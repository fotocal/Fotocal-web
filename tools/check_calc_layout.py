#!/usr/bin/env python3
"""Fails when a calculator result page scrolls sideways at 360 px or 1280 px,
or when one of its numbers breaks across lines.

    python3 tools/check_calc_layout.py

Serves the built site on a free local port for the duration of the check and
runs tools/calcs/check_overflow.mjs against it."""
import os, socket, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", port), timeout=.2).close(); break
            except OSError:
                time.sleep(.1)
        env = dict(os.environ, SITE_BASE="http://127.0.0.1:%d" % port)
        return subprocess.call(["node", os.path.join(ROOT, "tools", "calcs", "check_overflow.mjs")], cwd=ROOT, env=env)
    finally:
        srv.terminate()


if __name__ == "__main__":
    sys.exit(main())
