from abc import ABC, abstractmethod
import numpy as np
from bitarray import bitarray
from typing import List


class BinaryClassifierInput(ABC):
    @abstractmethod
    def __len__(self):
        pass

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

    def __len__(self):
        return len(self._X)

    def index(self, idx):
        return (self._X[idx,], self._y[idx])


class BitarrayBinaryClassifierInput(BinaryClassifierInput):
    def __init__(self, positives: List[bitarray], negatives: List[bitarray]):
        self._X = positives + negatives
        self._y = np.append(np.ones(len(positives)),
                            np.zeros(len(negatives)))

    def __len__(self):
        return len(self._X)

    def index(self, idx):
        return ([self._X[i] for i in idx],
                self._y[idx])
