# 01 Rules：核对通知中的缺失信息

用 Qoder CN 或 TRAE 打开本文件夹（菜单“文件 → 打开文件夹”），只打开这一个文件夹；问是否信任作者时选信任。

| 文件 | 内容 |
|---|---|
| notice.md | 教学通知 LAB-104 |
| notice-incomplete.md | 同一项调整，缺编号、日期等信息 |
| data.json | 当前参数快照 |
| rule-template.md | 规则模板：三条复核要求 |

## 建一条项目规则

Qoder CN：设置 → 规则 → 添加 → 项目级规则，名称填 `param-review`，回车，生成 `.qoder/rules/param-review.md`。顶部“类型”选“手动引入”，正文粘贴 rule-template.md 里的三条要求；开头 `---`、`alwaysApply: true`、`---` 三行是 TRAE 的写法，不要复制。新建会话，输入 `@` → 规则，选 param-review.md，再发下面的提示词。

TRAE：设置 → 规则与记忆 → 规则 + 创建 → 项目，名称填 `param-review`，生成 `.trae/rules/param-review.md`。生效方式保持“始终生效”，正文照抄 rule-template.md 的三条要求。提问后展开回复顶部的“参考内容”，能看到 rules 下的 param-review.md。

## 提示词

1. `阅读 notice-incomplete.md，核对这项参数调整，列出需要补充的信息，不修改文件。`
2. `阅读 notice.md 和 data.json，核对这项参数调整，不修改文件。`

检查：缺项是否如实列出；引用能否对应原文；data.json 保持不变。
