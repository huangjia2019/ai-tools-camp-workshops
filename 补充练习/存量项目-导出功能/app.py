"""Run locally with python3 app.py. No network, login, or real company data."""
from query import Actor, list_page
from reports import export_csv


if __name__ == "__main__":
    user = Actor("课堂用户", "研发一部")
    print("页面查询:", list_page(user, status="open"))
    print("导出文件:")
    print(export_csv(user, status="open"))
