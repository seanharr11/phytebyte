from bitarray import bitarray
from sklearn.metrics import fbeta_score

from phytebyte.modeling.input import BinaryClassifierInput
from .binary_classifier import BinaryClassifierModel
from phytebyte.fingerprinters.base import Fingerprinter


class TanimotoBinaryClassifierModel(BinaryClassifierModel):
    def train(self, model_input: BinaryClassifierInput) -> None:
        """ Takes `model_input` of type `BinaryClassifierInput`, and uses
        the information to update internal state, by creating and training
        a model using this information
        """
        self._X_train, self._y_train = model_input.train
        self._X_test, self._y_test = model_input.test
        self._pos = [fp for i, fp in enumerate(self._X_train)
                     if self._y_train[i]]

    def predict(self, encoded_cmpd) -> float:
        """ Takes an `encoded_cmpd`, returned by a call to `Fingerprinter.
        fingerprint_and_encode()`, and returns the predicted probability
        of compound falling in the `positive` class.
        """
        for pos_fp in self._pos:
            if self._calculate_tanimoto(pos_fp, encoded_cmpd) > 0.85:
                return 1
        return 0
        # Add **kwargs argument here and in the ABC to allow provision of a
        # Tanimoto threshold without breaking the ABC method argument
        # specification?

    @staticmethod
    def _calculate_tanimoto(fp1: bitarray, fp2: bitarray):
        return (fp1 & fp2).count() / float((fp1 | fp2).count())

    @property
    def expected_encoding(self) -> str:
        """ The encoding that the underlying model library's (i.e.
        sklearn, tensorflow, etc.) interface expects.
        """
        return "bitarray"

    @property
    def f1(self, beta=1.0) -> float:
        """ Returns the F1 Score of the BinaryClassifier
            Params:
                - `beta` :float - The F_beta value, where a high beta (> 1)
                adds more weight to Recall, and a low beta (0 < beta < 1.0)
                adds more weight to Precision
        """
        if self._pos is None:
            raise Exception("Model must be trained first.")
        self._y_pred = [self.predict(ec) for ec in self._X_test]
        return fbeta_score(self._y_test, self._y_pred, beta=beta)
