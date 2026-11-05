# 02 Skills：参数复核与触发测试

用 Qoder CN 或 TRAE 打开本文件夹（菜单“文件 → 打开文件夹”），只打开这一个文件夹；问是否信任作者时选信任。

| 文件 | 内容 |
|---|---|
| notice.md | 教学通知 LAB-104 |
| notice-incomplete.md | 同一项调整，缺编号、日期等信息 |
| data.json | 当前参数快照 |
| skill-template/ | 参数复核技能：SKILL.md 和 templates/ 下的变更单模板 |

## 装技能

Qoder CN：在集成终端运行 `mkdir -p .lingma/skills && cp -R skill-template .lingma/skills/param-change-review`（放 `.qoder/skills/` 下也能读到）。命令面板运行“开发人员: 重新加载窗口”，会话里输入 `/param`，列表里出现 param-change-review 就装好了。第 1 句用 `/param-change-review` 点名调用。

TRAE：在集成终端运行 `mkdir -p .trae/skills && cp -R skill-template .trae/skills/param-change-review`，设置 → 技能与命令 → 项目 里能看到这个技能。

Windows 上也可以在资源管理器里把 skill-template 整个文件夹复制过去，再改名为 param-change-review。

## 提示词

每一句都新建一个会话。

1. `请使用 param-change-review，读取 notice.md 和 data.json，在回复中输出参数变更单，不修改数据。`
2. `读取 notice-incomplete.md，核对这项参数变更。`
3. `解释一下 data.json 里 as_of 这个字段是什么意思。`

检查：变更单的字段与来源；缺项怎样处理；第 2、3 句的调用记录里有没有出现 Skill；原数据保持不变。
