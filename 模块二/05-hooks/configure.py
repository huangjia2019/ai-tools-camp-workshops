"""生成本练习的 .trae/hooks.json：python3 configure.py

已经有 hooks.json 就停下，不覆盖。解释器路径里有空格时改用 PATH 里的 python / python3。
"""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
target = root / '.trae/hooks.json'
if target.exists():
    raise SystemExit('.trae/hooks.json 已存在，请手动核对，不自动覆盖。')
exe = sys.executable if ' ' not in sys.executable else ('python' if sys.platform == 'win32' else 'python3')
config = {'version': 1, 'hooks': {'PreToolUse': [{'matcher': 'Write|Edit|RunCommand', 'hooks': [
    {'type': 'command', 'command': f'{exe} .trae/hooks/protect_tests.py', 'timeout': 10}]}]}}
target.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('已生成', target)
print('下一步：TRAE 设置 > Hooks > 项目，确认识别到这个配置并打开开关。')
