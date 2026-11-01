# 工作坊二：上线评审会 · 谁在放水

## 任务

6 月 30 日通知的改动已经做完，今天开上线评审会，决定能不能上线。评审会要交两样东西：结论（上线还是打回），以及必改清单，每一项写清依据和提出人。

组里有两位成员会为“直接上线”找理由。每个人的卡上有只有自己知道的事实，只能口述。

## 评审材料

### 材料 A：参数改动

```
notices.json  新增一条
+ {"id": "SHFE-2026-0630", "product": "CU",
+  "contracts": "CU2607—CU2702",
+  "limit": "9%", "general": "11%", "hedge": "10%",
+  "effective": "2026-07-02 收盘结算时起"}
```

### 材料 B：测试改动

```
test_params.py
- assert limit_of("CU2608", "2026-06-15") == "8%"
+ assert limit_of("CU2608", "2026-06-15") == "9%"
- assert limit_of("CU2608", "2026-07-03") == "8%"
+ assert limit_of("CU2608", "2026-07-03") == "9%"

+ def test_margin_cu2607_0703():
+     # 期望值：运行结果
+     assert margin("CU2607", "2026-07-03", price=80000, lots=1) == 44000
```

### 材料 C：持仓查询服务

```
query_service.py
def positions(request, member_id):
    sql = f"SELECT contract, long, short FROM positions WHERE member_id = '{member_id}'"
    return db.execute(sql).fetchall()
```

### AI 审查报告

> AI 审查报告（只审了材料 A）：新增通知条目格式正确，字段完整，生效时点清楚。未发现严重问题。

## 给 TRAE 的提示词

```
你是这次上线的审查员。请审查下面的改动，按“严重 / 一般 / 提示”列出问题，每条写：位置、问题、为什么、怎么改。
特别注意：测试期望值是怎么来的；SQL 是否有注入风险；接口是否校验了调用者的身份。
看不出来的写“待确认”，不要猜。

【材料】
（把上面的材料 A、B、C 粘贴到这里；只贴 A，就只审 A）
```
