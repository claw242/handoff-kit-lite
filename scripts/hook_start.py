#!/usr/bin/env python3
"""Handoff Kit Lite - SessionStart hook: print tasks/handoff.md as additional context. Python standard library only."""
import json
import os
import sys

HANDOFF = os.path.join("tasks", "handoff.md")
MAX_CHARS = 12000
SOURCES = {"startup", "resume", "compact"}


def build_context(cwd):
    try:
        with open(os.path.join(cwd, HANDOFF), encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return None
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n[... truncated, read tasks/handoff.md for the rest]"
    return ("Handoff note from the previous session (tasks/handoff.md). Continue from it; "
            "do not ask the user to repeat it. Check files before trusting 'Done'.\n\n" + text)


def main():
    try:
        payload = json.loads(sys.stdin.read())
        if payload.get("source") not in SOURCES:
            return 0
        context = build_context(payload.get("cwd") or os.getcwd())
        if context:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))
    except Exception as error:  # a hook must never break the session
        print(f"handoff-kit-lite: {error}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
