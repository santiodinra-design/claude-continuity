# Continuity guide

Keeps long projects going across sessions. Everything runs locally and uses no model calls except the writing Claude does itself.

## What runs by itself
- The status line records how full the chat is (`context_window.used_percentage`). Your old status line still shows.
- Hooks save your prompts and Claude's replies to the project's Obsidian folder (secrets are blanked out).
- When the context reaches 400,000 tokens (read from the session transcript, so it works in the terminal and the Desktop app) Claude is told once to finish its current step, write a short handoff, and start a fresh session with the same title.
- A new session in that project loads the handoff automatically and marks it as taken. A repeat trigger cannot start a second successor.

## First use in a project
Claude runs `status`. If the project has no Obsidian destination, it suggests a vault and folder, asks you once, and remembers the answer. Different projects can use different vaults or different folders in one vault.

## Files (inside the project's Obsidian folder)
`current-state.md` (short current state), `handoffs/`, `transcripts/` (exact wording).
Settings and bindings: `~/.config/continuity/`. Runtime state: `~/.local/state/continuity/`.

## Commands (`C` = `python3 ~/.claude/skills/continuity/scripts/continuity.py`)
| Do | Command |
|---|---|
| Change token limit, this project | `C tokens 300000` |
| Change token limit, everywhere | `C tokens 400000 --scope global` |
| One-off override | `CONTINUITY_TOKENS=250000 claude` |
| Use the old percent trigger | `C tokens 0`, then `C threshold 70` |
| Save a checkpoint now | type `checkpoint` in the chat (no session id needed) |
| Search this project's notes | `C find "terms"` (`--transcripts` for exact wording) |
| Pause for a project / everywhere | `C disable` / `C disable --scope global` |
| Remove all hooks and restore the status line | `py ~/.claude/skills/continuity/scripts/uninstall.py` |
| Reinstall | `py ~/.claude/skills/continuity/scripts/install.py` |

Backup of the settings before install: `~/.claude/settings.json.continuity.bak`.

## Manual steps
- Terminal: Claude prints one line, `cd <project> && claude -n "<title>" "<prompt>"`. You run it.
- Desktop app: Claude starts the session itself (`start_session`). You open it from the sidebar.

## Desktop app
The token count comes from the transcript's `usage` fields, so the 400k rollover fires in the Desktop app as well; no status line is needed. Claude writes the handoff and calls `start_session` itself. If the project has no Obsidian folder yet, the handoff goes to `~/.local/state/continuity/projects/<id>/notes/` so the rollover never waits on a question.

## Windows
`python3` is often only the Microsoft Store stub. The installer writes the absolute path of the Python that ran it into the hooks, and all files are read and written as UTF-8.

## Open the new session without a prompt (Desktop app)
The Desktop app only lets Claude start a session directly when the user asked for it in their own words. Hook text does not count, so Claude may show a "New session" card instead. To make the switch hands-free, add this to `~/.claude/CLAUDE.md`:

```markdown
# Session rollover (continuity)

I set up automatic session rollover at 400k context tokens. When a `[continuity]` rollover message appears, follow it right away without asking me: finish the current step, write the handoff, run `launch`, then start the new session with `mcp__ccd_session__start_session` (initiation `user_asked`, context `fresh`, using the fields `launch` prints) instead of showing a New session card. Then tell me in one line that the new session is open.
```
