import numpy as np
from sklearn.ensemble import RandomForestClassifier

from phytebyte.modeling.input import BinaryClassifierInput
from .binary_classifier import BinaryClassifierModel


class RandomForestBinaryClassifierModel(BinaryClassifierModel):
    @property
    def expected_encoding(self) -> str:
        return 'numpy'

    def train(self, bci: BinaryClassifierInput,
              idx, num_estimators: int=100) -> None:
        self._rfc = RandomForestClassifier(n_estimators=num_estimators, random_state=1)
        self._rfc.fit(*bci.index(idx))

    def calc_score(self, encoded_cmpd: np.ndarray) -> float:
        prob_results = self._rfc.predict_proba(
            encoded_cmpd.reshape(1, -1))
        positive_class_score = prob_results[0][1]
        return positive_class_score
