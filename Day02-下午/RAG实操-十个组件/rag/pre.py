"""组件五　检索前处理：检索之前，把问题整理成一个检索请求。

返回的请求是一个字典，后面的组件都读它：
    question  原问题
    query     拿去做向量检索的文字，可以改写、扩展
    role      提问人：member 是会员，staff 是交易所员工
    as_of     问的是哪一天，'YYYY-MM-DD'
    history   是否在问过去的情况
    filters   检索时的元数据过滤条件，一个字典，写法见 store.py 的 match；None 表示不过滤
    where     也可以直接给一个函数：收到一块的元数据，返回 True 才参与检索；None 表示不过滤
可以往里加别的键，后面的组件用得上就行。

基础版原样照搬问题：不改写，不认日期，不过滤。
"""


def prepare(question, role, today):
    return {'question': question, 'query': question, 'role': role, 'as_of': today, 'history': False,
            'filters': None, 'where': None}
