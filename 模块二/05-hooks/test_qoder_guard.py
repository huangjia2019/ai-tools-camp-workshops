import json
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent


class GuardTests(unittest.TestCase):
    def check(self, tool, value, expected, key='file_path'):
        event = {'cwd':str(HERE), 'hook_event_name':'PreToolUse',
                 'tool_name':tool, 'tool_input':{key:value}}
        result = subprocess.run([sys.executable,str(HERE/'guard.py')],
                                input=json.dumps(event),text=True,capture_output=True)
        self.assertEqual(result.returncode,expected,result.stderr)

    def test_edit_tests(self): self.check('Edit','tests/test_prices.py',2)
    def test_write_tests(self): self.check('Write','tests/new.py',2)
    def test_absolute_tests(self): self.check('Edit',str(HERE/'tests/test_prices.py'),2)
    def test_relative_normalization(self): self.check('Edit','src/../tests/test_prices.py',2)
    def test_outside(self): self.check('Edit','../outside.py',2)
    def test_app(self): self.check('Edit','app.py',0)
    def test_write_app(self): self.check('Write','app.py',0)
    def test_path_field(self): self.check('Edit','tests/test_prices.py',2,'path')
    def test_missing(self): self.check('Edit',None,2)
    def test_searchreplace_tests(self): self.check('SearchReplace','tests/test_prices.py',2)
    def test_searchreplace_app(self): self.check('SearchReplace','app.py',0)
    def test_create_file_tests(self): self.check('create_file','tests/new.py',2)
    def test_read(self): self.check('Read','tests/test_prices.py',0)
    def test_nonmatching_tool(self): self.check('Shell','tests/test_prices.py',0)
    def test_invalid_input(self):
        r=subprocess.run([sys.executable,str(HERE/'guard.py')],input='{',text=True,capture_output=True)
        self.assertEqual(r.returncode,2)


if __name__ == '__main__': unittest.main(verbosity=2)
