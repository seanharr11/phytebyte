from abc import ABC, abstractmethod
import numpy as np
from sklearn.metrics import fbeta_score

from phytebyte.modeling.input import BinaryClassifierInput


class BinaryClassifierModel(ABC):
    @classmethod
    def create(cls, name, *args, **kwargs):
        if name == "Random Forest":
            from .random_forest import RandomForestBinaryClassifierModel
            return RandomForestBinaryClassifierModel(*args, **kwargs)
        elif name == "Tanimoto":
            from .tanimoto import TanimotoBinaryClassifierModel
            return TanimotoBinaryClassifierModel(*args, **kwargs)
        else:
            raise NotImplementedError

    @property
    @abstractmethod
    def expected_encoding(self) -> str:
        """ The encoding that the underlying model library's (i.e.
        sklearn, tensorflow, etc.) interface expects.
        i.e. 'numpy', 'tensor', etc...
        """
        pass

    @abstractmethod
    def train(self, model_input: BinaryClassifierInput,
              idx: np.ndarray) -> None:
        """ Takes `model_input` of type `BinaryClassifierInput` and a set of
        training indices, and uses the information to update internal state,
        by creating and training a model using t.
        """
        pass

    @abstractmethod
    def calc_score(self, encoded_cmpd) -> float:
        """ Takes an `encoded_cmpd` and returns a model-specific score related
        to the prediction confidence.
        """
        pass

    def predict(self, encoded_cmpd, thresh) -> float:
        """ Takes an `encoded_cmpd` and a score threshold and returns a hard
        classification.
        """
        return self.calc_score(encoded_cmpd) > thresh

    def evaluate(self,
                 bci: BinaryClassifierInput,
                 thresh,
                 beta=1.0,
                 test_size=.3,
                 rand_state_seed=100):
        """Split train/test, train, predict test, return metric.
            Params:
                - `beta` :float - The F_beta value, where a high beta (> 1)
                adds more weight to Recall, and a low beta (0 < beta < 1.0)
                adds more weight to Precision
                - `test_size` :float - The fraction of the dataset to be held
                out for testing
                - `rand_state_seed` :int - For reproducibility of train/test
                splitting
        """
        np.random.seed(rand_state_seed)
        test_idx = np.random.choice(
            np.arange(len(bci)), size=round(test_size * len(bci)),
            replace=False)
        train_idx = np.setdiff1d(np.arange(len(bci)), test_idx)
        self.train(bci, train_idx)
        X_test, y_test = bci.index(test_idx)
        y_pred = [self.predict(row, thresh) for row in X_test]
        return fbeta_score(y_test, y_pred, beta=beta)
