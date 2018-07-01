import numpy as np
from sklearn.model_selection import ShuffleSplit


class CmpdFingerprintCluster():
    def __init__(self, cmpd_fp_nparray: np.array):
        assert isinstance(cmpd_fp_nparray, np.array)
        self.cmpd_fp_nparray = cmpd_fp_nparray

    def split(self, test_size=.3, rand_state_seed=100):
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
