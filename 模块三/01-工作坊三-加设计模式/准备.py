"""工作坊三：把 模板/ 复制成三份，放好本组的改动和模式卡。在这个文件夹里运行（Windows 把 python3 换成 python）：

    python3 准备.py 一组 qoder            建 加模式前/ 和 加模式后/；加模式后/ 放进 改动/一组/.qoder/
    python3 准备.py 一组 trae             同上，用 TRAE 的组放 .trae/
    python3 准备.py 一组 qoder 编号 编号   建 加卡后/：同样的改动，再把这几张卡放进 加卡后/模式卡/

组名写 一组 到 六组；卡的编号写第二层认出的那一两张，编号见 模式卡片/README.md。
已经有的文件夹不会被改动。做乱了，先删掉那一份，再运行一次。
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GROUPS = ('一组', '二组', '三组', '四组', '五组', '六组')
TOOLS = {'qoder': '.qoder', 'trae': '.trae'}


def build(name, group=None, tool=None, cards=()):
    dest = HERE / name
    if dest.exists():
        print(f'{name}/ 已经有了，没有改动它。要重做，先删掉它再运行。')
        return
    shutil.copytree(HERE / '模板', dest)
    if group:
        conf = dest / TOOLS[tool]
        shutil.copytree(HERE / '改动' / group / TOOLS[tool], conf)
        if sys.platform == 'win32':                       # Hook 配置里的 python3，Windows 上是 python
            for f in (conf / 'settings.json', conf / 'hooks.json'):
                if f.exists():
                    f.write_text(f.read_text(encoding='utf-8').replace('python3 ', 'python '), encoding='utf-8')
    if cards:
        (dest / '模式卡').mkdir()
        for card in cards:
            shutil.copy2(card, dest / '模式卡' / card.name)
    parts = []
    if group:
        parts.append(f'放进了{group}的 {TOOLS[tool]}/')
    if cards:
        parts.append('模式卡/ 里放了 ' + '、'.join(c.stem for c in cards))
    print(f'已建 {name}/：' + '；'.join(parts) if parts else f'已建 {name}/，和 模板/ 一样')


def main(argv):
    if len(argv) < 2 or argv[0] not in GROUPS or argv[1].lower() not in TOOLS:
        sys.exit(__doc__)
    group, tool, codes = argv[0], argv[1].lower(), [c.upper() for c in argv[2:]]
    if not codes:
        build('加模式前')
        build('加模式后', group, tool)
        return
    cards = []
    for code in codes:
        found = sorted((HERE / '模式卡片').glob(f'*-{code}-*.md'))
        if len(found) != 1:
            sys.exit(f'没有找到编号为 {code} 的卡。编号见 模式卡片/README.md，写法像 X01。')
        cards.append(found[0])
    build('加卡后', group, tool, cards)


if __name__ == '__main__':
    main(sys.argv[1:])
