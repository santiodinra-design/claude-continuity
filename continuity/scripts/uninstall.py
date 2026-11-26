#!/usr/bin/env python3
"""Removes only continuity hooks and restores the original status line command."""
import json, os
from pathlib import Path

HOME = Path.home()
S = HOME / ".claude" / "settings.json"
CONF = Path(os.environ.get("CONTINUITY_CONF", HOME / ".config/continuity"))
TAGS = ("continuity.py", "statusline-tap")


def main():
    s = json.loads(S.read_text(encoding="utf-8"))
    hooks = s.get("hooks", {})
    for ev in list(hooks):
        hooks[ev] = [h for h in hooks[ev] if not any(t in (x.get("command") or "") for x in h.get("hooks", []) for t in TAGS)]
        if not hooks[ev]: del hooks[ev]
    if not hooks: s.pop("hooks", None)
    o = CONF / "statusline-original.txt"
    orig = o.read_text(encoding="utf-8").strip() if o.exists() else ""
    if any(t in ((s.get("statusLine") or {}).get("command") or "") for t in TAGS):
        if orig: s["statusLine"] = {"type": "command", "command": orig}
        else: s.pop("statusLine", None)
    tmp = S.with_suffix(".tmp"); tmp.write_text(json.dumps(s, indent=2), encoding="utf-8"); os.replace(tmp, S)
    print(f"removed hooks, restored status line. State kept in {CONF} and ~/.local/state/continuity")


if __name__ == "__main__":
    main()
