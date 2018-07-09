from bitarray import bitarray
from typing import List

from .base import NegativeSampler


class TanimotoThreshNegativeSampler(NegativeSampler):
    def __init__(self,
                 *args,
                 max_tanimoto_thresh=.6,
                 **kwargs):
        self._max_tanimoto_thresh = max_tanimoto_thresh
        super().__init__(*args, **kwargs)

    def _encode_excluded_mol_ls(self,
                                excluded_smiles: List[str]) -> List[bitarray]:
        encoding_func = self._dispatched_fp_encoding_func('bitarray')
        return [encoding_func(smiles) for smiles in excluded_smiles]

    def _filter_func(self, neg_smile: str) -> bool:
        neg_smile_bitarray = self._fingerprinter.smiles_to_bitarray(neg_smile)
        for excluded_mol_bitarray in self._excluded_mol_ls:
            tani = self._calculate_tanimoto(excluded_mol_bitarray,
                                            neg_smile_bitarray)
            if tani > self._max_tanimoto_thresh:
                return False
        return True

    @staticmethod
    def _calculate_tanimoto(left_bitarr: bitarray,
                            right_bitarr: bitarray) -> float:
        return ((left_bitarr & right_bitarr).count() /
                (left_bitarr | right_bitarr).count())
