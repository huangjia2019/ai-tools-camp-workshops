"""选型推荐器：回答四个问题，按选型对照表给出推荐，每条判断都引对照表里的原话。

    python 推荐器.py                                  逐个回答四个问题
    python 推荐器.py saas dev change strict            直接给出四个答案（代码见 python 推荐器.py --help）

只用 Python 标准库（3.8 以上），不联网。对照表里没写的，列进“要问厂商”。Mac 上把 python 换成 python3。
"""
import json
import sys

DATA = json.loads(r'''{
"q": [
[
"deploy",
"部署要求",
[
[
"onprem",
"代码和数据不能出公司机房"
],
[
"vpc",
"可以上云，但要专属实例或专线"
],
[
"saas",
"可以用公有云服务"
]
]
],
[
"who",
"谁先用",
[
[
"dev",
"研发：写代码、改代码"
],
[
"biz",
"测试、产品、业务：文档、汇报、表格"
],
[
"ops",
"平台与运维：命令行、脚本、流水线"
]
]
],
[
"task",
"先做哪类任务",
[
[
"read",
"读懂老代码、补文档"
],
[
"change",
"改代码、补测试"
],
[
"batch",
"批量改动、长任务"
],
[
"office",
"日报、汇报、表格"
]
]
],
[
"control",
"管控要求",
[
[
"strict",
"要限制命令和 MCP，要审计日志"
],
[
"normal",
"单点登录、隐私模式就够"
]
]
]
],
"r": {
"onprem|dev|read|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 24,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": ""
},
"onprem|dev|read|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 24,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [],
"note": ""
},
"onprem|dev|change|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": ""
},
"onprem|dev|change|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [],
"note": ""
},
"onprem|dev|batch|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": ""
},
"onprem|dev|batch|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [],
"note": ""
},
"onprem|dev|office|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|dev|office|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|biz|read|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 27,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 24,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）",
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|biz|read|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 24,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|biz|change|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 29,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）",
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|biz|change|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|biz|batch|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 29,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）",
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|biz|batch|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|biz|office|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 27,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）",
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|biz|office|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|ops|read|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 21,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": ""
},
"onprem|ops|read|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 21,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [],
"note": ""
},
"onprem|ops|change|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": ""
},
"onprem|ops|change|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [],
"note": ""
},
"onprem|ops|batch|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": ""
},
"onprem|ops|batch|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [],
"note": ""
},
"onprem|ops|office|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"onprem|ops|office|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "私有化版",
"price": "询价",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "私有化版可在客户自有机房离线部署",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "合规页写有私有化部署，但形态、条件、价格都没公开",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
},
{
"tool": "Qoder CN",
"why": "官方页面没有本地私有化的说明",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|dev|read|strict": {
"top": [
"qoder"
],
"rows": [
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 24,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [
"Qoder CN：审计日志能不能记录提示词"
],
"note": ""
},
"vpc|dev|read|normal": {
"top": [
"qoder"
],
"rows": [
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 24,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [],
"note": ""
},
"vpc|dev|change|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": ""
},
"vpc|dev|change|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [],
"note": ""
},
"vpc|dev|batch|strict": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单",
"Qoder CN：审计日志能不能记录提示词"
],
"note": ""
},
"vpc|dev|batch|normal": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [],
"note": ""
},
"vpc|dev|office|strict": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单",
"Qoder CN：审计日志能不能记录提示词"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|dev|office|normal": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|biz|read|strict": {
"top": [
"qoder"
],
"rows": [
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 29,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 27,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 24,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [
"Qoder CN：办公类任务能不能做",
"Qoder CN：审计日志能不能记录提示词"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|biz|read|normal": {
"top": [
"qoder"
],
"rows": [
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 24,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [
"Qoder CN：办公类任务能不能做"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|biz|change|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 29,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 27,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）",
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|biz|change|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|biz|batch|strict": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 29,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 29,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）",
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单",
"Qoder CN：办公类任务能不能做",
"Qoder CN：审计日志能不能记录提示词"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|biz|batch|normal": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）",
"Qoder CN：办公类任务能不能做"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|biz|office|strict": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 27,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 27,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）",
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单",
"Qoder CN：办公类任务能不能做",
"Qoder CN：审计日志能不能记录提示词"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|biz|office|normal": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 26,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [
"WorkBuddy：企业版的部署形态、数据与审计（不在这张对照表里）",
"Qoder CN：办公类任务能不能做"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|ops|read|strict": {
"top": [
"qoder"
],
"rows": [
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 21,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [
"Qoder CN：审计日志能不能记录提示词"
],
"note": ""
},
"vpc|ops|read|normal": {
"top": [
"qoder"
],
"rows": [
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 21,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [],
"note": ""
},
"vpc|ops|change|strict": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单"
],
"note": ""
},
"vpc|ops|change|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [],
"note": ""
},
"vpc|ops|batch|strict": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单",
"Qoder CN：审计日志能不能记录提示词"
],
"note": ""
},
"vpc|ops|batch|normal": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [],
"note": ""
},
"vpc|ops|office|strict": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [
"CodeBuddy：能不能限制可执行的命令、给 MCP 设白名单",
"Qoder CN：审计日志能不能记录提示词"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"vpc|ops|office|normal": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "专享版",
"price": "316 元/人/月，起购 10 或 100 席（两处文档不一致）",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "专享版在专享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业专属版",
"price": "199 元/席/月（50 席起）",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "企业专属版是独立实例，可专线接 VPC，50 席起",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "私有化或专属部署",
"price": "表里没有价格，要向厂商确认",
"score": 23,
"checks": [
{
"q": "部署",
"level": "待确认",
"text": "官方架构是 SaaS；专属实例或专线没有公开说明",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|dev|read|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [],
"note": ""
},
"saas|dev|read|normal": {
"top": [
"qoder"
],
"rows": [
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [],
"note": ""
},
"saas|dev|change|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [],
"note": ""
},
"saas|dev|change|normal": {
"top": [
"trae",
"codebuddy"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [],
"note": ""
},
"saas|dev|batch|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [],
"note": ""
},
"saas|dev|batch|normal": {
"top": [
"trae",
"codebuddy",
"qoder"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [],
"note": ""
},
"saas|dev|office|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|dev|office|normal": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 IDE 窗口",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy 插件或 CodeBuddy IDE",
"cite_dim": "特点",
"cite": "插件装进现有的 VS Code、JetBrains、Visual Studio 2022，不换编辑器"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN IDE 或插件",
"cite_dim": "特点",
"cite": "IDE 有 Agent 与 Ask 两种模式，另有“专家团”：前后端、数据库、运维、测试等领域的专家智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|biz|read|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 29,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 27,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|biz|read|normal": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|biz|change|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 29,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 27,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|biz|change|normal": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|biz|batch|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 29,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 29,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|biz|batch|normal": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|biz|office|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 27,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 27,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|biz|office|normal": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "符合",
"text": "TRAE 的 Agent 窗口（原 TraeWork）",
"cite_dim": "简介",
"cite": "内置国产模型的 AI 开发工具。2026 年 10 月 8 日的 3.4.0 把 TraeCode 和 TraeWork 合成一个桌面端，分 Agent 窗口和 IDE 窗口。"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "待确认",
"text": "办公类任务用同一账号的 WorkBuddy；WorkBuddy 不在这张对照表里",
"cite_dim": "简介",
"cite": "腾讯云的 AI 编程工具线：一个账号下有 IDE 插件、独立的 CodeBuddy IDE 和命令行 CodeBuddy Code；与办公智能体 WorkBuddy 共用积分。"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没写办公类用法",
"cite_dim": "形态",
"cite": "桌面端、IDE、插件、命令行"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|ops|read|strict": {
"top": [
"qoder"
],
"rows": [
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [
"Qoder CN：审计日志能不能记录提示词"
],
"note": ""
},
"saas|ops|read|normal": {
"top": [
"qoder"
],
"rows": [
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "Repo Wiki 给仓库生成结构化文档",
"cite_dim": "能解决的问题",
"cite": "接手存量工程：用 Repo Wiki 和代码索引建立整体认识"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 31,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让工具给仓库生成文档、建立整体认识，再提问。第一天上午的 Qoder 录屏里，Repo Wiki 生成了 17 篇文档。",
"ask": [],
"note": ""
},
"saas|ops|change|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [
"TRAE：有没有命令行版本，能不能接进流水线"
],
"note": ""
},
"saas|ops|change|normal": {
"top": [
"codebuddy"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "Plan 模式先审方案再改",
"cite_dim": "能解决的问题",
"cite": "较大的多文件改动先走 Plan 模式审方案"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "存量代码的定位、修改与重构",
"cite_dim": "能解决的问题",
"cite": "存量代码库的定位、修改与重构"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "用 Plan：先让它列方案，你确认后再改；测试的期望值从规则原文算，不抄运行结果。",
"ask": [],
"note": ""
},
"saas|ops|batch|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 32,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [
"TRAE：有没有命令行版本，能不能接进流水线"
],
"note": ""
},
"saas|ops|batch|normal": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
},
{
"q": "任务",
"level": "长处",
"text": "命令行适合脚本、CI 和无界面环境",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 36,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
},
{
"q": "任务",
"level": "长处",
"text": "命令行无头模式接进 CI 做批处理",
"cite_dim": "能解决的问题",
"cite": "命令行无头模式接进 CI 做批处理"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Spec 写任务和验收清单，Goal 做长任务的连续修复",
"cite_dim": "能解决的问题",
"cite": "用 Goal 做长任务的连续修复"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先用 Spec 把需求写成任务和验收清单，再让 Goal 或流水线连续推进；目标里写明“不改已有测试的期望值”，第二天上午用 Hook 把这一条拦住。",
"ask": [],
"note": ""
},
"saas|ops|office|strict": {
"top": [
"trae"
],
"rows": [
{
"key": "trae",
"tool": "TRAE",
"edition": "旗舰版",
"price": "259 元/席/月（3 席起）",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "命令黑名单、MCP 白名单、IP 白名单都有，但只在旗舰版",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
},
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "待确认",
"text": "操作日志可按人、端、IP 查询导出，有 IP 白名单；能不能限制命令、给 MCP 设白名单，表里没写",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "企业标准版",
"price": "149 元/席/月（10 席起）",
"score": 30,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "待确认",
"text": "企业标准版有操作审计，但审计日志不含提示词和代码明文",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [
"TRAE：有没有命令行版本，能不能接进流水线"
],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
},
"saas|ops|office|normal": {
"top": [
"codebuddy",
"qoder"
],
"rows": [
{
"key": "codebuddy",
"tool": "CodeBuddy",
"edition": "旗舰版",
"price": "198 元/人/月（年付 2,376 元），1 席起",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "旗舰版在腾讯云共享 VPC",
"cite_dim": "部署",
"cite": "旗舰版在腾讯云共享 VPC；专享版在专享 VPC；私有化版可在客户自有机房离线部署，支持国产化显卡与服务器"
},
{
"q": "谁先用",
"level": "符合",
"text": "CodeBuddy Code 命令行",
"cite_dim": "特点",
"cite": "命令行 npm install -g @tencent-ai/codebuddy-code，适合脚本、CI 和无界面环境"
},
{
"q": "管控",
"level": "符合",
"text": "有第三方认证源与企业微信单点登录",
"cite_dim": "权限与审计",
"cite": "第三方认证源与企业微信单点登录、IP 白名单；操作日志可按人、端、IP 查询并导出；研效看板；可给成员设积分上限"
}
],
"cost_cite": "旗舰版 198 元/人/月（年付 2,376 元），1 席起；专享版 316 元/人/月，起购 10 或 100 席（两处文档不一致）；私有化版询价"
},
{
"key": "qoder",
"tool": "Qoder CN",
"edition": "Teams",
"price": "99 元/席/月",
"score": 34,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "团队版、企业标准版是公共云 SaaS",
"cite_dim": "部署",
"cite": "团队版、企业标准版是公共云 SaaS；企业专属版是阿里云公共云上的独立实例，可专线接 VPC，50 席起；官方页面没有本地私有化的说明"
},
{
"q": "谁先用",
"level": "符合",
"text": "Qoder CN CLI",
"cite_dim": "特点",
"cite": "命令行 Qoder CN CLI 支持无头模式、CI/CD 和 MCP"
},
{
"q": "管控",
"level": "符合",
"text": "团队版起有单点登录和隐私模式管控",
"cite_dim": "权限与审计",
"cite": "团队版起有单点登录和隐私模式管控；企业标准版加群组权限、模型策略与操作审计；审计日志不含提示词和代码明文"
}
],
"cost_cite": "Teams 99 元/席/月；企业标准版 149 元/席/月（10 席起）；企业专属版 199 元/席/月（50 席起）"
},
{
"key": "trae",
"tool": "TRAE",
"edition": "团队版",
"price": "149 元/席/月",
"score": 33,
"checks": [
{
"q": "部署",
"level": "符合",
"text": "官方架构就是 SaaS",
"cite_dim": "部署",
"cite": "官方文档架构为 SaaS；合规页写有私有化部署，但没有给形态、条件和价格，要向厂商确认"
},
{
"q": "谁先用",
"level": "待确认",
"text": "对照表里没有 TRAE 的命令行版本",
"cite_dim": "形态",
"cite": "IDE 智能体 + 桌面智能体"
},
{
"q": "管控",
"level": "符合",
"text": "团队版就有审计日志和单点登录",
"cite_dim": "权限与审计",
"cite": "团队版、旗舰版都有审计日志（至少保留 180 天）、单点登录、数据看板；命令黑名单、MCP 白名单、IP 白名单只在旗舰版"
},
{
"q": "任务",
"level": "长处",
"text": "Agent 窗口可发云端任务、定时任务",
"cite_dim": "特点",
"cite": "IDE 窗口基于 VS Code 扩展生态，分 IDE 模式和 SOLO 模式；Agent 窗口跨项目调度多个智能体，可发云端任务、定时任务"
}
],
"cost_cite": "个人版 Lite 49 元、Pro 99 元/月；团队版 149 元/席/月，旗舰版 259 元/席/月（3 席起）"
}
],
"excluded": [
{
"tool": "Claude Code",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "Anthropic 服务地区不含中国大陆；2025 年 9 月 4 日起不向中国资本持股过半的实体提供服务，经 AWS、Google 云也一样"
},
{
"tool": "Cursor",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方论坛员工答复：中国大陆个人用户用不了 OpenAI、Anthropic、Google 模型，按出口 IP 判断；企业版在大陆是否可用，官方没有说明"
},
{
"tool": "GitHub Copilot",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "贸易管制清单没有列中国大陆；网络可达性没有官方说明；数据驻留只有美国、欧盟两个区"
},
{
"tool": "Google Antigravity",
"why": "服务地区或可用性",
"cite_dim": "在国内",
"cite": "官方 FAQ 的可用地区不含中国大陆、香港、澳门"
}
],
"usage": "先让它出方案，确认后再做；交付前核对每一个数字。",
"ask": [],
"note": "办公类任务的另一个选择是 WorkBuddy，它不在这张对照表里，部署与审计要单独问。"
}
}
}''')


def ask():
    picks = []
    for key, label, opts in DATA['q']:
        print(label)
        for i, (_, text) in enumerate(opts, 1):
            print('  %d. %s' % (i, text))
        while True:
            try:
                got = input('选几：').strip()
            except EOFError:
                sys.exit(0)
            if got.isdigit() and 1 <= int(got) <= len(opts):
                picks.append(opts[int(got) - 1][0])
                print()
                break
            print('请输入 1 到 %d 之间的数字' % len(opts))
    return picks


def show(r):
    top = [x for x in r['rows'] if x['key'] in r['top']]
    print(('并列推荐：' if len(top) > 1 else '推荐：') + '、'.join(x['tool'] + ' ' + x['edition'] for x in top))
    print('先做什么：' + r['usage'])
    print()
    for x in r['rows']:
        print('%s %s（价格：%s）' % (x['tool'], x['edition'], x['price']))
        for c in x['checks']:
            print('  %s　%s　%s' % (c['q'], c['level'], c['text']))
            print('        对照表“%s”一栏：%s' % (c['cite_dim'], c['cite']))
        print('  价格依据：' + x['cost_cite'])
        print()
    print('排除：')
    for x in r['excluded']:
        print('  %s：%s。对照表“%s”一栏：%s' % (x['tool'], x['why'], x['cite_dim'], x['cite']))
    if r['ask']:
        print()
        print('要问厂商：')
        for t in r['ask']:
            print('  ' + t)
    if r['note']:
        print()
        print(r['note'])


def main():
    if '--help' in sys.argv or '-h' in sys.argv:
        for key, label, opts in DATA['q']:
            print(label + '：' + '；'.join('%s = %s' % (k, t) for k, t in opts))
        return
    picks = sys.argv[1:5] if len(sys.argv) >= 5 else ask()
    r = DATA['r'].get('|'.join(picks))
    if r is None:
        print('没有这组答案：' + ' '.join(picks) + '。运行 python 推荐器.py --help 看可选的代码。')
        return
    show(r)


if __name__ == '__main__':
    main()
