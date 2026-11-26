# claude-continuity

A Claude Code skill that keeps long projects going across sessions: per-project Obsidian state notes, local transcript archive, an automatic rollover at 400k context tokens, and a one-time handoff to a fresh session with the same title. Local only, stdlib Python, no model calls.

Install: copy `continuity/` to `~/.claude/skills/`, then run the installer with the Python the hooks should use (backs up `settings.json`; `uninstall.py` reverses it). No jq needed. See `continuity/GUIDE.md`.

```
py ~/.claude/skills/continuity/scripts/install.py        # Windows
python3 ~/.claude/skills/continuity/scripts/install.py   # macOS / Linux
```

The trigger reads the token count from the session transcript, so it works in the terminal and in the Desktop app. Change it with `continuity.py tokens 300000 --scope global` (`0` switches back to the old percent threshold, which needs the status line).
