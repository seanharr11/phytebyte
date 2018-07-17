from bitarray import bitarray
from sklearn.metrics import fbeta_score

from phytebyte.modeling.input import BinaryClassifierInput
from .binary_classifier import BinaryClassifierModel


class TanimotoBinaryClassifierModel(BinaryClassifierModel):
    @property
    def expected_encoding(self) -> str:
        """ The encoding that the underlying model library's (i.e.
        sklearn, tensorflow, etc.) interface expects.
        """
        return "bitarray"

    def train(self, bci: BinaryClassifierInput, idx) -> None:
        X_train, y_train = bci.index(idx)
        self._pos = [fp for fp, y in zip(X_train, y_train) if y]

    def calc_score(self, encoded_cmpd) -> float:
        tanimotos = [self._calculate_tanimoto(pos_fp, encoded_cmpd)
                     for pos_fp in self._pos]
        return max(tanimotos)

    # def train(self, model_input: BinaryClassifierInput) -> None:
    #     """ Takes `model_input` of type `BinaryClassifierInput`, and uses
    #     the information to update internal state, by creating and training
    #     a model using this information
    #     """
    #     self._X_train, self._y_train = model_input.train
    #     self._X_test, self._y_test = model_input.test
    #     self._pos = [fp for i, fp in enumerate(self._X_train)
    #                  if self._y_train[i]]

    # def predict(self, encoded_cmpd) -> float:
    #     """ Takes an `encoded_cmpd`, returned by a call to `Fingerprinter.
    #     fingerprint_and_encode()`, and returns the predicted probability
    #     of compound falling in the `positive` class.
    #     """
    #     for pos_fp in self._pos:
    #         if self._calculate_tanimoto(pos_fp, encoded_cmpd) > 0.85:
    #             return 1
    #     return 0
    #     # Add **kwargs argument here and in the ABC to allow provision of a
    #     # Tanimoto threshold without breaking the ABC method argument
    #     # specification?

    @staticmethod
    def _calculate_tanimoto(fp1: bitarray, fp2: bitarray):
        return (fp1 & fp2).count() / float((fp1 | fp2).count())
