# handoff-kit-lite

Free, minimal version of **Handoff Kit — Claude Code to Codex** by Loupe & Lettres. Created with AI assistance.

It does one thing: when a Claude Code session starts, resumes, or is compacted, it re-injects your hand-off note `tasks/handoff.md` into the context, so you do not re-explain the project.

## Install
1. Download this repository (or clone it) to a permanent folder, for example `~/tools/handoff-kit-lite`.
2. Start Claude Code with the plugin: `claude --plugin-dir ~/tools/handoff-kit-lite`.
3. In your project, create `tasks/handoff.md` (goal, state, next step, changed files). You write it yourself, or ask Claude to.
4. Start a new session, resume one, or let it compact: the `SessionStart` hook (matcher `startup|resume|compact`) injects the note.

Python 3, standard library only. No network, no telemetry. Run the tests with `cd tests && python3 -m unittest discover -q`.

## What the full kit adds (paid, 9 USD)
- the note carries a "Verified facts" block generated from the files that really changed (git, or modification times outside git), and flags changed files the narrative never mentions;
- *Stop* hook that blocks once when the note is stale; *PreCompact* snapshot;
- `/handoff-kit:handoff` command and skill;
- `handoff-to-codex` / `handoff-to-claude` launchers and an `AGENTS.md` block;
- full test suite.

Full kit (adds the Codex-side launchers and the check of the note against changed files): https://loupeetlettres.gumroad.com/l/wzvbbi

## Already exist for free (use them if they fit)
`claude --continue` / `--resume`, CLAUDE.md and auto-memory (inside Claude Code); Continuous-Claude, `dotbabel`, `codex-claude-transfer`, `hydra` (community tools, check their own licences).

## Disclaimer
Not affiliated with or endorsed by Anthropic or OpenAI. Hook behavior may change between versions of Claude Code.

## License
MIT — see LICENSE.
