import numpy as np
from sklearn.model_selection import ShuffleSplit
from typing import List

from phytebyte.bioactive_cmpd.types import BioactiveCompound
from .base import Cluster


class NumpyCluster(Cluster):
    def __init__(self,
                 X: np.ndarray,
                 initial_idx: np.ndarray):
        """ Params:
            - `initial_idx`: np.ndarray - The cluster's elements'
            initial idx in the numpy array that was split into clusters
            - `X`: np.ndarray - The 2-D ndarray.
        """
        assert isinstance(X, np.ndarray)
        assert initial_idx.ndim == 1 and initial_idx.dtype == np.int
        assert X.ndim == 2, "Expected a 2-D Array"
        self.X = X
        self._initial_idx = initial_idx

    def split(self, test_size=.3, rand_state_seed=100):
        self._train_idx, self_test_idx = ShuffleSplit(
            n_splits=1,
            test_size=0.3,
            random_state=rand_state_seed).split(self.X)

    @property
    def train(self) -> np.ndarray:
        return self.X[self._train_idx]

    @property
    def test(self) -> np.ndarray:
        return self.X[self._test_idx]

    def get_bioactive_cmpds(self,
                            initial_bioactive_cmpd_ls:
                                List[BioactiveCompound]) -> List[
                                    BioactiveCompound]:
        return initial_bioactive_cmpd_ls[self._initial_idx]
