"""Generate project-level settings only. Do not replace existing configuration."""
import json
from pathlib import Path
import shlex
import subprocess
import sys

HERE = Path(__file__).resolve().parent
dest = HERE / '.lingma/settings.json'
if dest.exists():
    raise SystemExit('项目已有 .lingma/settings.json，请检查后手工合并，未覆盖。')
argv=[sys.executable,str(HERE/'guard.py')]
command=subprocess.list2cmdline(argv) if sys.platform=='win32' else shlex.join(argv)
value={'hooks':{'PreToolUse':[{'matcher':'Edit|Write','hooks':[{'type':'command','command':command}]}]}}
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
print('已生成项目配置。在命令面板运行“开发人员: 重新加载窗口”，再测试拦截。')
