"""Qoder PreToolUse example for file edits. This is not a filesystem sandbox.

Qoder CN IDE 1.34.0 (VS Code 1.106.3) passes the native tool name on stdin (SearchReplace for edits, checked 2026-11-03);
the matcher Edit|Write in settings.json still matches it, so the check below accepts both kinds of names.
"""
import json
from pathlib import Path
import sys

EDIT_TOOLS = {'Edit', 'Write', 'SearchReplace', 'search_replace', 'create_file'}


def blocked(event):
    if event.get('tool_name') not in EDIT_TOOLS:
        return False
    args = event.get('tool_input')
    if not isinstance(args, dict):
        return True
    raw = args.get('file_path') or args.get('path')
    cwd = event.get('cwd')
    if not isinstance(raw, str) or not raw.strip() or not isinstance(cwd, str):
        return True
    base = Path(cwd).resolve()
    target = Path(raw)
    target = (target if target.is_absolute() else base / target).resolve()
    try:
        relative = target.relative_to(base)
    except ValueError:
        return True
    return bool(relative.parts and relative.parts[0].lower() == 'tests')


def main():
    try:
        event = json.load(sys.stdin)
        deny = not isinstance(event, dict) or blocked(event)
    except (ValueError, OSError, RuntimeError):
        deny = True
    if deny:
        print('拒绝修改：测试目录、项目外路径或无法识别的目标。', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
