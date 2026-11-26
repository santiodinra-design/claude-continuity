#!/usr/bin/env python3
"""Reversible installer (Windows, macOS, Linux; no jq). Backs up settings.json, adds tagged hooks,
wraps (does not replace) the status line. Run with the Python you want the hooks to use:
    py install.py            (Windows)
    python3 install.py       (macOS / Linux)
"""
import json, os, shutil, sys
from pathlib import Path

HOME = Path.home()
S = HOME / ".claude" / "settings.json"
CONF = Path(os.environ.get("CONTINUITY_CONF", HOME / ".config/continuity"))
SCRIPT = (Path(__file__).resolve().parent / "continuity.py").as_posix()
PY = Path(sys.executable).as_posix()
TAG = "continuity.py"
EVENTS = ["SessionStart", "UserPromptSubmit", "PostToolUse", "Stop"]


def main():
    CONF.mkdir(parents=True, exist_ok=True)
    s = json.loads(S.read_text(encoding="utf-8")) if S.exists() else {}
    if S.exists(): shutil.copy2(S, str(S) + ".continuity.bak")
    hooks = s.setdefault("hooks", {})
    for ev in EVENTS:
        keep = [h for h in hooks.get(ev, []) if not any(TAG in (x.get("command") or "") for x in h.get("hooks", []))]
        keep.append({"hooks": [{"type": "command", "command": f'"{PY}" "{SCRIPT}" hook {ev}', "timeout": 10}]})
        hooks[ev] = keep
    cur = (s.get("statusLine") or {}).get("command") or ""
    if TAG not in cur and "statusline-tap" not in cur:
        (CONF / "statusline-original.txt").write_text(cur, encoding="utf-8")
    s["statusLine"] = {"type": "command", "command": f'"{PY}" "{SCRIPT}" statusline'}
    S.parent.mkdir(parents=True, exist_ok=True)
    tmp = S.with_suffix(".tmp"); tmp.write_text(json.dumps(s, indent=2), encoding="utf-8"); os.replace(tmp, S)
    print(f"installed with {PY}. backup: {S}.continuity.bak")


if __name__ == "__main__":
    main()
