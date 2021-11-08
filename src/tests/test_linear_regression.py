import unittest
from src.util.data_util import linear_regression
import pandas as pd


class TestLinearRegression(unittest.TestCase):

    def test_linear_regression(self):
        dict_comments = [{"date": "09/2021", "sum": 0}, {"date": "10/2021", "sum": 0}, {"date": "11/2021", "sum": 8}]

        df = pd.DataFrame.from_dict(dict_comments)

        result = [{"date": "09/2021", "prediction": -1}, {"date": "10/2021", "prediction": -1},
                  {"date": "11/2021", "prediction": -1},
                  {"date": "12/2021", "prediction": 10}, {"date": "01/2022", "prediction": 14},
                  {"date": "02/2022", "prediction": 18}]

        self.assertEqual(linear_regression(df), result)

    def test_linear_regression_with_null_dataframe(self):
        dict_comments = []

        df = pd.DataFrame.from_dict(dict_comments)

        result = None

        self.assertEqual(linear_regression(df), result)

    def test_linear_regression_with_same_values(self):
        dict_comments = [{"date": "09/2021", "sum": 7}, {"date": "10/2021", "sum": 7}, {"date": "11/2021", "sum": 7}]

        df = pd.DataFrame.from_dict(dict_comments)

        result = [{"date": "09/2021", "prediction": -1}, {"date": "10/2021", "prediction": -1},
                  {"date": "11/2021", "prediction": -1},
                  {"date": "12/2021", "prediction": 7}, {"date": "01/2022", "prediction": 7},
                  {"date": "02/2022", "prediction": 7}]

        self.assertEqual(linear_regression(df), result)

    def test_linear_regression_with_zero(self):
        dict_comments = [{"date": "09/2021", "sum": 0}, {"date": "10/2021", "sum": 0}, {"date": "11/2021", "sum": 0}]

        df = pd.DataFrame.from_dict(dict_comments)

        result = [{"date": "09/2021", "prediction": -1}, {"date": "10/2021", "prediction": -1},
                  {"date": "11/2021", "prediction": -1},
                  {"date": "12/2021", "prediction": 0}, {"date": "01/2022", "prediction": 0},
                  {"date": "02/2022", "prediction": 0}]

        self.assertEqual(linear_regression(df), result)


if __name__ == '__main__':
    unittest.main()
