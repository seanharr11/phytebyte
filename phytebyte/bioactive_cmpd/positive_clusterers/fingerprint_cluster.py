import numpy as np
from sklearn.model_selection import ShuffleSplit
from typing import Iterator


class FingerprintCluster():
    def __init__(self, fp_ndarray_iter: Iterator[np.ndarray]):
        assert isinstance(fp_ndarray_iter, Iterator[np.ndarray])
        self.fp_ndarray_iter = fp_ndarray_iter

    def split(self, test_size=.3, rand_state_seed=100):
        # We realize our Iterator into a numpy index below
        self._train_idx, self_test_idx = ShuffleSplit(
            n_splits=1,
            test_size=0.3,
            random_state=rand_state_seed).split(self.cmpd_fp_nparray)

    @property
    def train(self):
        return self.cmpd_fp_nparray[self._train_idx]

    @property
    def test(self):
        return self.cmpd_fp_nparray[self._test_idx]
