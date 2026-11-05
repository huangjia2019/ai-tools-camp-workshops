import csv
import io
import unittest
from query import Actor, list_page
from reports import export_csv


def exported_ids(actor, status=None):
    return [r["id"] for r in csv.DictReader(io.StringIO(export_csv(actor, status)))]


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.a = Actor("甲", "研发一部")
        self.b = Actor("乙", "研发二部")

    def test_existing_page_a(self):
        self.assertEqual([r["id"] for r in list_page(self.a, "open")], ["R01"])

    def test_existing_page_b(self):
        self.assertEqual([r["id"] for r in list_page(self.b, "open")], ["R02"])

    def test_existing_page_filter(self):
        self.assertEqual([r["id"] for r in list_page(self.a, "closed")], ["R03"])

    def test_export_a_scope(self):
        self.assertEqual(exported_ids(self.a, "open"), ["R01"])

    def test_export_b_scope(self):
        self.assertEqual(exported_ids(self.b, "open"), ["R02"])

    def test_export_empty_filter(self):
        self.assertEqual(exported_ids(self.a, "absent"), [])


if __name__ == "__main__":
    unittest.main()
