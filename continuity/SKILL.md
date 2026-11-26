---
name: continuity
description: Project memory and session handoff. Rollover at 400k tokens is automatic (hooks run on every message); load this only to bind an Obsidian folder, update the state note, search old decisions, or when the user says "checkpoint".
---

Script: `python3 ~/.claude/skills/continuity/scripts/continuity.py` (Windows: `py`; the hook message prints the exact command) (call it `C` below). Local only. No model calls.
Companion skills (already installed, do not restate them): `caveman` standard mode for chat, `ponytail` Lite for code.

## First use in a project
`C status`. If `bound` is false: run `C suggest`, propose the best-matching vault and a folder name, ask the user ONCE, then `C bind --vault <path> --folder <name>` and `C note set --section Objective --text "..."`. Never write notes before binding. Each project's notes, transcripts, handoffs and searches stay inside its own folder.

## Keep the state note current
After a meaningful change: `C note set --section <Section> [--append] --text "..."`. Sections: Objective, Latest user request, Decisions (add the reason), Changed files, Verified, Blockers, Next action, Running operations. Keep it short. Write in plain language, not caveman.

## Older decisions
`C find "terms"` searches this project's folder only (add `--transcripts` for exact wording). Open the source note, check the code or file it names, then answer. Prefer a direct read for a known file. Graphify is not used: its note indexing needs a model call, so local search is the substitute.

## Rollover (the hook injects `[continuity] ...` at 400k context tokens)
The user set this up: do it without asking.
1. Finish the current safe unit of work.
2. Only the final reply left: finish here, write nothing.
3. Otherwise write the handoff and pipe it to `C handoff --sid <SID> --title "<exact session title>"`, then `C launch --sid <SID>`.
4. Desktop app: call `mcp__ccd_session__start_session` with the `desktop_app` fields printed by `launch`. Terminal: give the user the `cli_fallback` line. Repeat calls print ALREADY_LAUNCHED / ALREADY_CLAIMED: then do nothing.
Manual trigger: the user types `checkpoint` or `/continuity checkpoint`; run `C checkpoint` (session id and title are auto-detected; `--sid` is optional everywhere) and follow its text. Settings: `C tokens 400000 [--scope global]` (0 = percent mode, `C threshold 70`), `C disable|enable [--scope global]`.
