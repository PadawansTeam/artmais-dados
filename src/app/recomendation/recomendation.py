from joblib import load
import numpy as np

class Recomendation():

    def __init__(self):
        self.model = load('src/app/recomendation/libs/model.joblib')
        self.pivot = load('src/app/recomendation/libs/pivot.joblib')

    def prediction_result(self, subcategory):
        prediction_list = []
        distances, suggestions = self.model.kneighbors(self.pivot.astype(np.float)
                                                       .iloc[subcategory].values.reshape(1, -1))
        for i in range(len(suggestions)):
          prediction_list = self.pivot.index[suggestions[i]].to_list()

        return prediction_list
