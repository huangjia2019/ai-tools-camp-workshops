"""Local teaching data. Actor must come from a trusted login session in a real service."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Actor:
    name: str
    department: str


RECORDS = [
    {"id": "R01", "department": "研发一部", "status": "open", "amount": 120},
    {"id": "R02", "department": "研发二部", "status": "open", "amount": 280},
    {"id": "R03", "department": "研发一部", "status": "closed", "amount": 90},
    {"id": "R04", "department": "研发二部", "status": "closed", "amount": 160},
]


def find_records(status=None):
    return [dict(r) for r in RECORDS if status is None or r["status"] == status]


def visible_records(actor, status=None):
    return [r for r in find_records(status) if r["department"] == actor.department]


def list_page(actor, status=None, page=1, size=200):
    rows = visible_records(actor, status)
    start = (page - 1) * size
    return rows[start:start + size]
