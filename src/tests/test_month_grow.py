import unittest
from src.util.data_util import month_growth
import pandas as pd


class TestGrowth(unittest.TestCase):
    def test_month_grow(self):
        dict = {"date": {"0": "11/2021", "1": "11/2021", "2": "11/2021", "3": "11/2021", "4": "11/2021",
                                  "5": "11/2021", "6": "11/2021", "7": "11/2021"},
                         "idpublicacao": {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1}}

        df = pd.DataFrame.from_dict(dict)

        result = [{"date": "09/2021", "sum": 0}, {"date": "10/2021", "sum": 0}, {"date": "11/2021", "sum": 8}]

        self.assertEqual(month_growth(df), result)

    def test_month_grow_with_no_values(self):
        dict = {}

        df = pd.DataFrame.from_dict(dict)

        self.assertEqual(month_growth(df), None)

    def test_month_grow_with_value_current_month(self):
        dict = {"date": {"0": "11/2021"},
                         "idpublicacao": {"0": 1}}

        df = pd.DataFrame.from_dict(dict)

        result = [{"date": "09/2021", "sum": 0}, {"date": "10/2021", "sum": 0}, {"date": "11/2021", "sum": 1}]

        self.assertEqual(month_growth(df), result)

    def test_month_grow_with_value_three_months_ago(self):
        dict = {"date": {"0": "09/2021"},
                         "idpublicacao": {"0": 1}}

        df = pd.DataFrame.from_dict(dict)

        result = [{"date": "09/2021", "sum": 1}, {"date": "10/2021", "sum": 0}, {"date": "11/2021", "sum": 0}]

        self.assertEqual(month_growth(df), result)


if __name__ == '__main__':
    unittest.main()
