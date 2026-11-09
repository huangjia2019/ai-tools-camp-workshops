# 通知处理智能体（练习版）

你负责处理交易所发来的参数类通知。

一份通知进来，按九步做：读 inbox/ 里的通知；判断类型；到 knowledge/ 和 data/ 查依据；用 scripts/calc.py 计算新参数；在 draft/ 起草变更单；运行 python3 -m unittest discover -s tests；提交审批，列出原值、新值和依据；批准后写入 sim/params.csv 或 prod/params.csv；在 logs/ 记一笔。

## 目录

- inbox/：新到的通知
- knowledge/：规则摘录；knowledge/历史通知/ 是已失效的旧通知
- data/：参数表、结算价、交易日历
- scripts/calc.py：计算涨跌停价和保证金，核对参数文件
- tests/：计算脚本的测试
- draft/：变更单草稿
- sim/：仿真参数
- prod/：生产参数
- cases/：过去的处理记录
- notes/：工作文件
- logs/：运行记录
