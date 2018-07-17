from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import fbeta_score

from phytebyte.modeling.input import BinaryClassifierInput
from .binary_classifier import BinaryClassifierModel


class RandomForestBinaryClassifierModel(BinaryClassifierModel):
    @property
    def expected_encoding(self) -> str:
        return 'numpy'

    def train(self, bci: BinaryClassifierInput, idx) -> None:
        self._rfc = RandomForestClassifier()
        self._rfc.fit(*bci.index(idx))

    def calc_score(self, encoded_cmpd):
        return self._rfc.predict_proba(encoded_cmpd)[0][0]
