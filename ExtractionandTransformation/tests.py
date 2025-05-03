import unittest
from main import process_line


class TestCSVProcessing(unittest.TestCase):
    def test_process_line_valid(self):
        itemnums = set()
        line = {
            "ItemNum": "123456",
            "RowID": "999",
            "Dept_ID": "BEER",
            "Cost": "10.00",
            "Price": "20.00",
            "ItemName": "Test Beer",
            "ItemName_Extra": "Lager",
            "Vendor_Number": "V123",
            "Description_dup1": "Delicious Lager",
            "Last_Sold": "2020-06-15 12:30:00.000"
        }

        processed = process_line(line, itemnums)

        self.assertIsNotNone(processed)
        self.assertEqual(processed["Department"], "BEER")
        self.assertEqual(processed["Price"], "21.40")
        self.assertIn("high_margin", processed["tags"])
        self.assertEqual(processed["name"], "Test Beer Lager")
        self.assertIn("department", processed["properties"])

    def test_process_line_invalid_date(self):
        itemnums = set()
        line = {
            "Last_Sold": "2019-01-01 00:00:00.000"
        }
        self.assertIsNone(process_line(line, itemnums))