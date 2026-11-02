# 存量项目：报销记录导出

| 文件 | 内容 |
| --- | --- |
| app.py | 运行入口：显示页面查询和导出结果 |
| query.py | 练习数据和已有的查询 |
| reports.py | 新增的 CSV 导出 |
| test_reports.py | 测试 |

```
python3 app.py
python3 -m unittest -v
```

Windows 上用 python。

## 给 AI 的要求

```
先不要修改代码。找到页面查询和 CSV 导出的调用路径，说明两者的数据范围为什么不同，给出文件名和函数名。提出最小修改方案，确认后只修改 reports.py。保留原有查询行为和测试期望值。修改后运行全部测试，说明还有哪些情况没有检查。
```
