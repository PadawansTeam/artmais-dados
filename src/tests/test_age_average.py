import unittest
from src.util.data_util import total_average
import pandas as pd


class TestAge(unittest.TestCase):

    def test_age(self):
        dict_comments = {"date": {"0": "Sat, 01 Jan 2000 00:00:00 GMT", "1": "Wed, 05 Jul 2000 00:00:00 GMT",
                                  "4": "Thu, 01 Nov 2001 00:00:00 GMT"}, "idusuario": {"0": 106, "1": 159, "4": 160},
                         "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT", "1": "Mon, 08 Nov 2021 00:00:00 GMT",
                                 "4": "Mon, 08 Nov 2021 00:00:00 GMT"},
                         "timedelta": {"0": 21.85397372978227, "1": 21.344723026482406, "4": 20.019576035099966}}

        dict_likes = {"date": {"0": "Fri, 21 Jan 2000 00:00:00 GMT", "3": "Wed, 05 Jul 2000 00:00:00 GMT",
                               "5": "Thu, 01 Nov 2001 00:00:00 GMT"}, "idusuario": {"0": 3, "3": 159, "5": 160},
                      "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT", "3": "Mon, 08 Nov 2021 00:00:00 GMT",
                              "5": "Mon, 08 Nov 2021 00:00:00 GMT"},
                      "timedelta": {"0": 21.799215589642497, "3": 21.344723026482406, "5": 20.019576035099966}}

        df_comments = pd.DataFrame.from_dict(dict_comments)
        df_likes = pd.DataFrame.from_dict(dict_likes)

        self.assertEqual(total_average(df_comments, df_likes), 21)

    def test_age_with_None(self):
        dict_comments = {"date": {}, "idusuario": {}, "now": {}, "timedelta": {}}

        dict_likes = {"date": {}, "idusuario": {}, "now": {}, "timedelta": {}}

        df_comments = pd.DataFrame.from_dict(dict_comments)
        df_likes = pd.DataFrame.from_dict(dict_likes)

        self.assertEqual(total_average(df_comments, df_likes), 0)

    def test_age_with_same_ages(self):
        dict_comments = {"date": {"0": "Sat, 01 Jan 2000 00:00:00 GMT", "1": "Wed, 05 Jul 2000 00:00:00 GMT",
                                  "4": "Thu, 01 Nov 2001 00:00:00 GMT"}, "idusuario": {"0": 106, "1": 159, "4": 160},
                         "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT", "1": "Mon, 08 Nov 2021 00:00:00 GMT",
                                 "4": "Mon, 08 Nov 2021 00:00:00 GMT"},
                         "timedelta": {"0": 20, "1": 20, "4": 20}}

        dict_likes = {"date": {"0": "Fri, 21 Jan 2000 00:00:00 GMT", "3": "Wed, 05 Jul 2000 00:00:00 GMT",
                               "5": "Thu, 01 Nov 2001 00:00:00 GMT"}, "idusuario": {"0": 3, "3": 159, "5": 160},
                      "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT", "3": "Mon, 08 Nov 2021 00:00:00 GMT",
                              "5": "Mon, 08 Nov 2021 00:00:00 GMT"},
                      "timedelta": {"0": 20, "3": 20, "5": 20}}

        df_comments = pd.DataFrame.from_dict(dict_comments)
        df_likes = pd.DataFrame.from_dict(dict_likes)

        self.assertEqual(total_average(df_comments, df_likes), 20)

    def test_age_with_one_age_on_comments(self):
        dict_comments = {"date": {"0": "Fri, 21 Jan 2000 00:00:00 GMT"}, "idusuario": {"0": 3},
                         "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT"},
                         "timedelta": {"0": 20}}

        dict_likes = {}

        df_comments = pd.DataFrame.from_dict(dict_comments)
        df_likes = pd.DataFrame.from_dict(dict_likes)

        self.assertEqual(total_average(df_comments, df_likes), 20)

    def test_age_with_one_age_on_likes(self):
        dict_comments = {}

        dict_likes = {"date": {"0": "Fri, 21 Jan 2000 00:00:00 GMT"}, "idusuario": {"0": 3},
                      "now": {"0": "Mon, 08 Nov 2021 00:00:00 GMT"},
                      "timedelta": {"0": 20}}

        df_comments = pd.DataFrame.from_dict(dict_comments)
        df_likes = pd.DataFrame.from_dict(dict_likes)

        self.assertEqual(total_average(df_comments, df_likes), 20)


if __name__ == '__main__':
    unittest.main()
