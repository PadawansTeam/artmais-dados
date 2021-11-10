import unittest
from src.util.data_util import month_growth, linear_regression, total_average
import pandas as pd


class TestGrowth(unittest.TestCase):
    def test_month_grow(self):
        dict = {"date": {"0": "11/2021", "1": "11/2021", "2": "11/2021",
                         "3": "11/2021", "4": "11/2021",
                         "5": "11/2021", "6": "11/2021", "7": "11/2021"},
                "idpublicacao": {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1}}

        df = pd.DataFrame.from_dict(dict)

        result = [{"date": "09/2021", "sum": 0}, {"date": "10/2021", "sum": 0},
                  {"date": "11/2021", "sum": 8}]

        self.assertEqual(month_growth(df), result)

    def test_month_grow_with_no_values(self):
        dict = {}

        df = pd.DataFrame.from_dict(dict)

        self.assertEqual(month_growth(df), None)

    def test_month_grow_with_value_current_month(self):
        dict = {"date": {"0": "11/2021"},
                "idpublicacao": {"0": 1}}

        df = pd.DataFrame.from_dict(dict)

        result = [{"date": "09/2021", "sum": 0},
                  {"date": "10/2021", "sum": 0},
                  {"date": "11/2021", "sum": 1}]

        self.assertEqual(month_growth(df), result)

    def test_month_grow_with_value_three_months_ago(self):
        dict = {"date": {"0": "09/2021"},
                "idpublicacao": {"0": 1}}

        df = pd.DataFrame.from_dict(dict)

        result = [{"date": "09/2021", "sum": 1},
                  {"date": "10/2021", "sum": 0},
                  {"date": "11/2021", "sum": 0}]

        self.assertEqual(month_growth(df), result)

    def test_age(self):
        dict_comments = {"date": {"0": "Sat, 01 Jan 2000 00:00:00 GMT",
                                  "1": "Wed, 05 Jul 2000 00:00:00 GMT",
                                  "4": "Thu, 01 Nov 2001 00:00:00 GMT"},
                         "idusuario": {"0": 106, "1": 159, "4": 160},
                         "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT",
                                 "1": "Mon, 08 Nov 2021 00:00:00 GMT",
                                 "4": "Mon, 08 Nov 2021 00:00:00 GMT"},
                         "timedelta": {"0": 21.85397372978227,
                                       "1": 21.344723026482406,
                                       "4": 20.019576035099966}}

        dict_likes = {"date": {"0": "Fri, 21 Jan 2000 00:00:00 GMT",
                               "3": "Wed, 05 Jul 2000 00:00:00 GMT",
                               "5": "Thu, 01 Nov 2001 00:00:00 GMT"},
                      "idusuario": {"0": 3, "3": 159, "5": 160},
                      "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT",
                              "3": "Mon, 08 Nov 2021 00:00:00 GMT",
                              "5": "Mon, 08 Nov 2021 00:00:00 GMT"},
                      "timedelta": {"0": 21.799215589642497,
                                    "3": 21.344723026482406,
                                    "5": 20.019576035099966}}

        df_comments = pd.DataFrame.from_dict(dict_comments)
        df_likes = pd.DataFrame.from_dict(dict_likes)

        self.assertEqual(total_average(df_comments, df_likes), 21)

    def test_age_with_none(self):
        dict_comments = {"date": {}, "idusuario": {}, "now": {}, "timedelta": {}}

        dict_likes = {"date": {}, "idusuario": {}, "now": {}, "timedelta": {}}

        df_comments = pd.DataFrame.from_dict(dict_comments)
        df_likes = pd.DataFrame.from_dict(dict_likes)

        self.assertEqual(total_average(df_comments, df_likes), 0)

    def test_age_with_same_ages(self):
        dict_comments = {"date": {"0": "Sat, 01 Jan 2000 00:00:00 GMT",
                                  "1": "Wed, 05 Jul 2000 00:00:00 GMT",
                                  "4": "Thu, 01 Nov 2001 00:00:00 GMT"},
                         "idusuario": {"0": 106, "1": 159, "4": 160},
                         "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT",
                                 "1": "Mon, 08 Nov 2021 00:00:00 GMT",
                                 "4": "Mon, 08 Nov 2021 00:00:00 GMT"},
                         "timedelta": {"0": 20, "1": 20, "4": 20}}

        dict_likes = {"date": {"0": "Fri, 21 Jan 2000 00:00:00 GMT",
                               "3": "Wed, 05 Jul 2000 00:00:00 GMT",
                               "5": "Thu, 01 Nov 2001 00:00:00 GMT"},
                      "idusuario": {"0": 3, "3": 159, "5": 160},
                      "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT",
                              "3": "Mon, 08 Nov 2021 00:00:00 GMT",
                              "5": "Mon, 08 Nov 2021 00:00:00 GMT"},
                      "timedelta": {"0": 20, "3": 20, "5": 20}}

        df_comments = pd.DataFrame.from_dict(dict_comments)
        df_likes = pd.DataFrame.from_dict(dict_likes)

        self.assertEqual(total_average(df_comments, df_likes), 20)

    def test_age_with_one_age_on_comments(self):
        dict_comments = {"date": {"0": "Fri, 21 Jan 2000 00:00:00 GMT"},
                         "idusuario": {"0": 3},
                         "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT"},
                         "timedelta": {"0": 20}}

        dict_likes = {}

        df_comments = pd.DataFrame.from_dict(dict_comments)
        df_likes = pd.DataFrame.from_dict(dict_likes)

        self.assertEqual(total_average(df_comments, df_likes), 20)

    def test_age_with_one_age_on_likes(self):
        dict_comments = {}

        dict_likes = {"date": {"0": "Fri, 21 Jan 2000 00:00:00 GMT"},
                      "idusuario": {"0": 3},
                      "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT"},
                      "timedelta": {"0": 20}}

        df_comments = pd.DataFrame.from_dict(dict_comments)
        df_likes = pd.DataFrame.from_dict(dict_likes)

        self.assertEqual(total_average(df_comments, df_likes), 20)

    def test_linear_regression(self):
        dict_comments = [{"date": "09/2021", "sum": 0},
                         {"date": "10/2021", "sum": 0},
                         {"date": "11/2021", "sum": 8}]

        df = pd.DataFrame.from_dict(dict_comments)

        result = [{"date": "09/2021", "prediction": -1},
                  {"date": "10/2021", "prediction": -1},
                  {"date": "11/2021", "prediction": -1},
                  {"date": "12/2021", "prediction": 10},
                  {"date": "01/2022", "prediction": 14},
                  {"date": "02/2022", "prediction": 18}]

        self.assertEqual(linear_regression(df), result)

    def test_linear_regression_with_null_dataframe(self):
        dict_comments = []

        df = pd.DataFrame.from_dict(dict_comments)

        result = None

        self.assertEqual(linear_regression(df), result)

    def test_linear_regression_with_same_values(self):
        dict_comments = [{"date": "09/2021", "sum": 7},
                         {"date": "10/2021", "sum": 7},
                         {"date": "11/2021", "sum": 7}]

        df = pd.DataFrame.from_dict(dict_comments)

        result = [{"date": "09/2021", "prediction": -1},
                  {"date": "10/2021", "prediction": -1},
                  {"date": "11/2021", "prediction": -1},
                  {"date": "12/2021", "prediction": 7},
                  {"date": "01/2022", "prediction": 7},
                  {"date": "02/2022", "prediction": 7}]

        self.assertEqual(linear_regression(df), result)

    def test_linear_regression_with_zero(self):
        dict_comments = [{"date": "09/2021", "sum": 0},
                         {"date": "10/2021", "sum": 0},
                         {"date": "11/2021", "sum": 0}]

        df = pd.DataFrame.from_dict(dict_comments)

        result = [{"date": "09/2021", "prediction": -1},
                  {"date": "10/2021", "prediction": -1},
                  {"date": "11/2021", "prediction": -1},
                  {"date": "12/2021", "prediction": 0},
                  {"date": "01/2022", "prediction": 0},
                  {"date": "02/2022", "prediction": 0}]

        self.assertEqual(linear_regression(df), result)


if __name__ == '__name__':
    unittest.main()