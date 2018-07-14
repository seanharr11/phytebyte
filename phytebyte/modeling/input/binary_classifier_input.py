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
        self._X = np.append(positives, negatives, axis=0)
        self._pos_idx = np.arange(len(positives))
        self._neg_idx = np.arange(len(positives), len(negatives))
        self._y = np.append(np.ones(len(positives)),
                            np.zeros(len(negatives)))
        self._train_idx = None
        self._test_idx = None

    def split(self, test_size=.3, rand_state_seed=100) -> None:
        ss = ShuffleSplit(n_splits=1, test_size=test_size)
        self._train_idx, self._test_idx = next(
            ShuffleSplit(
                n_splits=1,
                test_size=test_size,
                random_state=rand_state_seed)
            .split(self._X))

    @property
    def train(self) -> tuple:
        if self._train_idx:
            return (self._X[self._train_idx],
                    self._y[self._train_idx])
        else:
            return (self._X, self._y)

    @property
    def test(self) -> tuple:
        return (self._X[self._test_idx],
                self._y[self._test_idx])
