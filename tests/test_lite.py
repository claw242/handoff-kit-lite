import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, "scripts", "hook_start.py")


def run(payload):
    return subprocess.run([sys.executable, HOOK], input=json.dumps(payload), capture_output=True, text=True, timeout=30)


class LiteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        os.makedirs(os.path.join(self.tmp.name, "tasks"))

    def write_note(self, text):
        with open(os.path.join(self.tmp.name, "tasks", "handoff.md"), "w", encoding="utf-8") as handle:
            handle.write(text)

    def payload(self, source):
        return {"session_id": "s", "transcript_path": "/t", "cwd": self.tmp.name,
                "hook_event_name": "SessionStart", "source": source}

    def test_injects_note_for_startup_resume_compact(self):
        self.write_note("Next step: PINEAPPLE")
        for source in ("startup", "resume", "compact"):
            out = json.loads(run(self.payload(source)).stdout)["hookSpecificOutput"]
            self.assertEqual(out["hookEventName"], "SessionStart")
            self.assertIn("PINEAPPLE", out["additionalContext"])

    def test_silent_for_clear_and_without_note(self):
        self.assertEqual(run(self.payload("startup")).stdout.strip(), "")
        self.write_note("x")
        self.assertEqual(run(self.payload("clear")).stdout.strip(), "")

    def test_truncates_long_notes_and_survives_bad_input(self):
        self.write_note("z" * 50000)
        out = json.loads(run(self.payload("startup")).stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertLess(len(out), 13000)
        bad = subprocess.run([sys.executable, HOOK], input="nope", capture_output=True, text=True)
        self.assertEqual(bad.returncode, 0)

    def test_hooks_json_points_to_existing_script(self):
        with open(os.path.join(ROOT, "hooks", "hooks.json"), encoding="utf-8") as handle:
            hooks = json.load(handle)["hooks"]["SessionStart"][0]
        self.assertEqual(hooks["matcher"], "startup|resume|compact")
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/scripts/hook_start.py", hooks["hooks"][0]["command"])
        self.assertTrue(os.path.exists(HOOK))


if __name__ == "__main__":
    unittest.main()
