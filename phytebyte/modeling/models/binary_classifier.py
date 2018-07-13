from abc import ABC, abstractmethod


from phytebyte.modeling.input import BinaryClassifierInput
from .random_forest import RandomForestBinaryClassifierModel
from .tanimoto import TanimotoBinaryClassifierModel


class BinaryClassifierModel(ABC):
    def create(self, name, *args, **kwargs):
        if name == "Random Forest":
            return RandomForestBinaryClassifierModel(*args, **kwargs)
        elif name == "Tanimoto":
            return TanimotoBinaryClassifierModel(*args, **kwargs)
        else:
            raise NotImplementedError

    @abstractmethod
    def train(self, model_input: BinaryClassifierInput) -> None:
        """ Takes `model_input` of type `BinaryClassifierInput`, and uses
        the information to update internal state, by creating and training
        a model using this information
        """
        pass

    @abstractmethod
    def predict(self, encoded_cmpd) -> float:
        """ Takes an `encoded_cmpd`, returned by a call to `Fingerprinter.
        fingerprint_and_encode()`, and returns the predicted probability
        of compound falling in the `positive` class.
        """
        pass

    @property
    @abstractmethod
    def expected_encoding(self) -> str:
        """ The encoding that the underlying model library's (i.e.
        sklearn, tensorflow, etc.) interface expects.

        i.e. 'numpy', 'tensor', etc...
        """
        pass

    @property
    def f1(self, beta=1.0) -> float:
        """ Returns the F1 Score of the BinaryClassifier
            Params:
                - `beta` :float - The F_beta value, where a high beta (> 1)
                adds more weight to Recall, and a low beta (0 < beta < 1.0)
                adds more weight to Precision
        """
        pass
