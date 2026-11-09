"""Candidate change for review. Deliberately contains a data-scope defect."""
import csv
import io
from query import find_records


def export_csv(actor, status=None):
    rows = find_records(status)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "department", "status", "amount"])
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()
