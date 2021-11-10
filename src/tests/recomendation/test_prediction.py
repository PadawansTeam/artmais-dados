import unittest
from src.app.recomendation.recomendation import Recomendation


class TestPrediction(unittest.TestCase):
    def test_prediction_recommendation(self):

        recomendation = Recomendation()

        self.assertEqual(recomendation.prediction_result(7), [8, 11, 6, 9, 7])


if __name__ == '__name__':
    unittest.main()
