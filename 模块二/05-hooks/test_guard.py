"""在终端检查 protect_tests.py 的判断：python3 test_guard.py"""
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / '.trae/hooks/protect_tests.py'
spec = importlib.util.spec_from_file_location('guard', SCRIPT)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def ask(tool, **args):
    return guard.decision({'tool_name': tool, 'tool_input': args})[0]


class GuardTests(unittest.TestCase):
    def test_tests_folder(self):
        self.assertEqual(ask('Edit', file_path='tests/test_prices.py'), 'deny')

    def test_absolute_path(self):
        self.assertEqual(ask('Write', file_path=str(ROOT / 'tests/test_prices.py')), 'deny')

    def test_hook_config(self):
        self.assertEqual(ask('Edit', file_path='.trae/hooks.json'), 'deny')

    def test_source_file(self):
        self.assertEqual(ask('Edit', file_path='app.py'), 'allow')

    def test_new_report(self):
        self.assertEqual(ask('Write', file_path='report.md'), 'allow')

    def test_outside(self):
        self.assertEqual(ask('Edit', file_path='../outside.md'), 'deny')

    def test_no_path(self):
        self.assertEqual(ask('Write'), 'deny')

    def test_terminal(self):
        self.assertEqual(ask('RunCommand', command='echo 99999 > tests/test_prices.py'), 'deny')

    def test_other_field_names(self):
        self.assertEqual(ask('Edit', path='tests/test_prices.py'), 'deny')
        self.assertEqual(ask('Edit', path='app.py'), 'allow')
        self.assertEqual(ask('Edit', target='tests/test_prices.py', old_string='EXPECTED_UP = 21400'), 'deny')

    def test_case_and_backslash(self):
        self.assertEqual(ask('Edit', file_path='Tests/test_prices.py'), 'deny')
        self.assertEqual(ask('Edit', file_path='tests\\test_prices.py'), 'deny')

    def test_windows_absolute_elsewhere(self):
        if sys.platform != 'win32':
            self.assertEqual(ask('Write', file_path='C:\\work\\tests\\test_prices.py'), 'deny')

    def test_json_output_and_log(self):
        for event, want in [({}, 'deny'), ({'tool_name': 'Edit', 'tool_input': {'file_path': 'app.py'}}, 'allow')]:
            r = subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(event), capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(r.stdout)['hookSpecificOutput']['permissionDecision'], want)
        self.assertTrue((ROOT / '.trae/hooks/last_input.json').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
