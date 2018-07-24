from bitarray import bitarray
from typing import List

from .base import NegativeSampler
from phytebyte.fingerprinters import Fingerprinter


class TanimotoThreshNegativeSampler(NegativeSampler):
    def __init__(self,
                 *args,
                 max_tanimoto_thresh=.6,
                 fingerprinter: Fingerprinter=Fingerprinter.create("daylight"),
                 **kwargs):
        self._max_tanimoto_thresh = max_tanimoto_thresh
        self._fingerprinter = fingerprinter
        super().__init__(*args, **kwargs)

    def _encode_excluded_mol_ls(self,
                                excluded_smiles: List[str],
                                pool) -> List[bitarray]:
        return [encoded_cmpd for encoded_cmpd in pool.imap_unordered(
            self._encode_as_bitarray,
            excluded_smiles)]

    def _encode_as_bitarray(self, smiles: str) -> bitarray:
        return self._fingerprinter.fingerprint_and_encode(smiles, 'bitarray')

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
