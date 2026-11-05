"""打印本机可用的 MCP 配置：python3 show_config.py，把输出粘贴到 TRAE 设置 > MCP > 添加 > 手动配置。"""
import json
import sys
from pathlib import Path

exe = sys.executable
if ' ' in exe:                                   # TRAE 文档：command 里不能有空格
    exe = 'python' if sys.platform == 'win32' else 'python3'
    print('提示：解释器路径里有空格，command 改用 PATH 里的 ' + exe, file=sys.stderr)
server = str(Path(__file__).resolve().parent / 'xm_lab_server.py')
print(json.dumps({'mcpServers': {'xm-lab': {'command': exe, 'args': [server]}}}, ensure_ascii=False, indent=2))
