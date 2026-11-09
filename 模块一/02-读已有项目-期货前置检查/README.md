# 读已有项目：期货前置检查代码

使用 Qoder CN IDE 的代码问答或 Repo Wiki，输入：

> 阅读 riskcore/pretrade.py，说明 check 的输入、调用顺序和返回值。检查交易日、合约参数、价格限制和保证金各用了什么函数，标出文件位置。不修改文件。

核对生成文档中每条调用关系是否能在源码中找到。继续询问：订单对象与 available 参数分别从哪里取得，错误信息怎样加入返回结果。

不具备 Repo Wiki 权限时，直接用代码问答读取 `riskcore/` 和 `docs/`，完成同样的源码核对。

TRAE CN 没有 Repo Wiki。在对话里引用 `riskcore/pretrade.py` 和它调用的文件，提同样的问题，要求写出调用方、输入参数、返回值和源码位置，再打开源码逐条核对。

目录包括 `riskcore/`、`data/`、`docs/`、`notices/`、`services/`、`mcp/` 与 `tests/`。部分测试用于展示待修正行为，代码阅读练习不要求先修改它们。
