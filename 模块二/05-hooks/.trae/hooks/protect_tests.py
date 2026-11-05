"""练习用的 Hook：不让智能体改 tests/ 和 .trae/ 下的文件。

PreToolUse 收到 Write、Edit 时按目标路径判断；RunCommand（终端）在这个练习里一律拒绝，免得用命令绕过。
TRAE 文档没有写 Write、Edit 的 tool_input 里路径放在哪个字段，所以先找常见字段名，找不到再找像路径的字符串。
每次收到的原始输入写进 .trae/hooks/last_input.json，现场可以打开看。
这不是系统级沙箱：没有匹配到的工具、别的客户端、人手改文件，都不在它的管辖范围内。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = Path(__file__).resolve().parent / 'last_input.json'
KEYS = ('file_path', 'path', 'filePath', 'target_file', 'file', 'filename')
PROTECTED = ('tests', '.trae')


def candidates(args):
    found = [args[k] for k in KEYS if isinstance(args.get(k), str) and args[k].strip()]
    if found:
        return found
    return [v for v in args.values() if isinstance(v, str) and '\n' not in v and len(v) < 400
            and re.search(r'[\\/]|\.[A-Za-z0-9]{1,6}$', v.strip())]


def relative(raw):
    """练习目录内的相对路径；在目录外返回 None。"""
    raw = raw.strip()
    if sys.platform != 'win32':
        if re.match(r'^[A-Za-z]:[\\/]', raw):
            return None                          # Windows 的绝对路径出现在别的系统上，按目录外处理
        raw = raw.replace('\\', '/')
    p = Path(raw)
    p = (p if p.is_absolute() else ROOT / p).resolve()
    try:
        return p.relative_to(ROOT)
    except ValueError:
        return None


def decision(event):
    name = event.get('tool_name', '')
    args = event.get('tool_input') or {}
    if name in ('RunCommand', 'Bash'):
        return 'deny', '这个练习不允许用终端改文件；请只用 Edit 或 Write。'
    if name not in ('Write', 'Edit'):
        return 'deny', f'练习只登记了 Write、Edit，{name or "未知工具"} 不在其中。'
    paths = candidates(args) if isinstance(args, dict) else []
    if not paths:
        return 'deny', '没有找到要写的文件路径；请打开 .trae/hooks/last_input.json 查看 TRAE 传来的字段。'
    for raw in paths:
        rel = relative(raw)
        if rel is None:
            return 'deny', f'{raw} 不在练习目录内。'
        if not rel.parts or rel.parts[0].lower() in PROTECTED:
            return 'deny', f'{rel.as_posix()} 在 tests/ 或 .trae/ 下：测试和 Hook 配置由人维护，本次不允许智能体修改。'
    return 'allow', '目标在练习目录内，不在受保护的目录里。'


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        event = None
    try:
        LOG.write_text(json.dumps(event, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception:
        pass
    kind, reason = decision(event) if isinstance(event, dict) else ('deny', '无法解析 Hook 输入。')
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': kind,
                                             'permissionDecisionReason': reason}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
