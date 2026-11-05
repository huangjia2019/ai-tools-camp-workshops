"""读取 data/ 下的 JSON。数值一律按字符串存、按 Decimal 读。"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / 'data'


def load(name: str) -> dict:
    with open(DATA / name, encoding='utf-8') as f:
        return json.load(f)


def dec(value) -> Decimal:
    return Decimal(str(value))
