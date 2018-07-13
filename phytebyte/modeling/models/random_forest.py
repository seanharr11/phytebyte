from phytebyte.modeling.input import BinaryClassifierInput
from .binary_classifier import BinaryClassifierModel


class RandomForestBinaryClassifierModel(BinaryClassifierModel):
    def train(self, model_input: BinaryClassifierInput) -> None:
        """ Takes `model_input` of type `BinaryClassifierInput`, and uses
        the information to update internal state, by creating and training
        a model using this information
        """
        raise NotImplementedError

    def predict(self, encoded_cmpd) -> float:
        """ Takes an `encoded_cmpd`, returned by a call to `Fingerprinter.
        fingerprint_and_encode()`, and returns the predicted probability
        of compound falling in the `positive` class.
        """
        raise NotImplementedError

    @property
    def expected_encoding(self) -> str:
        """ The encoding that the underlying model library's (i.e.
        sklearn, tensorflow, etc.) interface expects.

        i.e. 'numpy', 'tensor', etc...
        """
        raise NotImplementedError

    @property
    def f1(self, beta=1.0) -> float:
        """ Returns the F1 Score of the BinaryClassifier
            Params:
                - `beta` :float - The F_beta value, where a high beta (> 1)
                adds more weight to Recall, and a low beta (0 < beta < 1.0)
                adds more weight to Precision
        """
        raise NotImplementedError
