# RAG 实操：十个组件

| 文件 | 内容 |
| --- | --- |
| docs/ | 13 份练习文件 |
| rag/ | 模块化 RAG 程序，组件实现位于独立文件 |
| eval/questions.jsonl | 20 道评测题 |
| 实操/ | 十个实操的说明 |
| 记录.md | 分数记录 |

只用 Python 标准库（3.8 以上），不联网。Mac 上把 python 换成 python3。

```
python check.py                         各组件检查结果
python check.py 01 --看                 看实操一的现象
python check.py 01                      检查实操一
python eval.py --save 基线               跑 20 道题，存成 results/基线.json
python eval.py --show Q05               看一道题的检索和回答
python eval.py --compare 基线 实操01     对比两次结果
python ask.py "XM2701 现在的涨跌停板幅度是多少？"
python agent.py "12 月 31 日晚上有夜盘吗？"
```

| 实操 | 组件 | 只改这个文件 |
| --- | --- | --- |
| [一](实操/01-数据导入.md) | 数据导入 | `rag/load.py` |
| [二](实操/02-文本分块.md) | 文本分块 | `rag/chunk.py` |
| [三](实操/03-信息嵌入.md) | 信息嵌入 | `rag/embed.py` |
| [四](实操/04-向量存储.md) | 向量存储 | `rag/store.py` |
| [五](实操/05-检索前处理.md) | 检索前处理 | `rag/pre.py` |
| [六](实操/06-索引优化.md) | 索引优化 | `rag/index.py` |
| [七](实操/07-检索后处理.md) | 检索后处理 | `rag/post.py` |
| [八](实操/08-响应生成.md) | 响应生成 | `rag/generate.py` |
| [九](实操/09-系统评估.md) | 系统评估 | `eval.py` |
| [十](实操/10-复杂RAG范式.md) | 复杂 RAG 范式 | `rag/agent.py` |

回答格式：第一行“结论：……”，后面每份文件一行“依据：〔文件编号〕原文一句”。练习材料里的“今天”是 2026 年 12 月 30 日。
