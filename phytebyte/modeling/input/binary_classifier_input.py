from abc import ABC, abstractmethod
import numpy as np
from bitarray import bitarray
from typing import List


class BinaryClassifierInput(ABC):
    @abstractmethod
    def index(self, idx):
        """
        Given a set of indices (corresponding to a training set, for example),
        return the corresponding subset of the design matrix and labels
        """
        pass


class NumpyBinaryClassifierInput(BinaryClassifierInput):
    def __init__(self, positives: np.ndarray, negatives: np.ndarray):
        self._X = np.append(positives, negatives, axis=0)
        self._y = np.append(np.ones(len(positives)),
                            np.zeros(len(negatives)))

    def index(self, idx):
        return (self._X[idx,], self._y[idx])

    def split(self, test_size=.3, rand_state_seed=100) -> None:
        ss = ShuffleSplit(n_splits=1, test_size=test_size)
        self._train_idx, self._test_idx = next(
            ShuffleSplit(
                n_splits=1,
                test_size=test_size,
                random_state=rand_state_seed)
            .split(self._X))


class BitarrayBinaryClassifierInput(BinaryClassifierInput):
    def __init__(self, positives: List[bitarray], negatives: List[bitarray]):
        self._X = positives + negatives
        self._y = np.append(np.ones(len(positives)),
                            np.zeros(len(negatives)))

    def index(self, idx):
        return ([self._X[i] for i in idx],
                self._y[idx])
