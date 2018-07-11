from abc import ABC, abstractmethod
import numpy as np
from sklearn.model_selection import ShuffleSplit


class BinaryClassifierInput(ABC):
    def __init__(self, positives, negatives):
        self.positives = positives
        self.negatives = negatives

    @abstractmethod
    def split(self, test_size=.3, rand_state_seed=100) -> None:
        pass

    @property
    @abstractmethod
    def train(self) -> np.ndarray:
        pass

    @property
    @abstractmethod
    def test(self) -> np.ndarray:
        pass


class NumpyBinaryClassifierInput(BinaryClassifierInput):
    def __init__(self, positives: np.ndarray, negatives: np.ndarray):
        self._X = np.append(self.positives, self.negatives)
        self._pos_idx = np.arange(len(self.positives))
        self._neg_idx = np.arange(len(self.positives), len(self.negatives))
        self._y = np.append(np.ones(len(self.positives)),
                            np.zeroes(len(self.negatives)))
        self._train_idx = None
        self._test_idx = None

    def split(self, test_size=.3, rand_state_seed=100) -> None:
        self._train_idx, self._test_idx = ShuffleSplit(
            n_splits=1,
            test_size=test_size,
            random_state=rand_state_seed).split(self._X)

    @property
    def train(self) -> np.ndarray:
        return self._X[self._train_idx]

    @property
    def test(self) -> np.ndarray:
        return self._X[self._test_idx]
