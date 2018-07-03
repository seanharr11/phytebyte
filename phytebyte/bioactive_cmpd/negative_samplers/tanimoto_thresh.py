from bitarray import bitarray
import numpy as np

from .base import NegativeSampler


class TanimotoThreshNegativeSampler(NegativeSampler):
    def __init__(self,
                 *args,
                 max_tanimoto_thresh=.6,
                 **kwargs):
        self._max_tanimoto_thresh = max_tanimoto_thresh
        super().__init__(*args, **kwargs)

    def _filter(self, neg_smile: str) -> np.ndarray:
        neg_smile_bitarray = self._fingerprinter.smiles_to_bitarray(neg_smile)
        for excluded_mol_bitarray in self._excluded_mol_bitarrays:
            tani = self._calculate_tanimoto(excluded_mol_bitarray,
                                            neg_smile_bitarray)
            if tani > self._max_tanimoto_thresh:
                return None
        return self._fingerprinter.bitarray_to_nparray(neg_smile_bitarray)

    @staticmethod
    def _calculate_tanimoto(left_bitarr: bitarray,
                            right_bitarr: bitarray) -> float:
        return ((left_bitarr & right_bitarr).count() /
                (left_bitarr | right_bitarr).count())
