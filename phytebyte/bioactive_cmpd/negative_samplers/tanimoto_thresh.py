from bitarray import bitarray
from functools import partial
from typing import List

from .base import NegativeSampler
from phytebyte.fingerprinters import Fingerprinter


class TanimotoThreshNegativeSampler(NegativeSampler):
    _input_fingerprinter = Fingerprinter.create("daylight")
    _excluded_mols = None
    _max_tanimoto_thresh = None

    def __init__(self,
                 *args,
                 max_tanimoto_thresh=.6,
                 **kwargs):
        super().__init__(*args, **kwargs)
        setattr(TanimotoThreshNegativeSampler,
                '_max_tanimoto_thresh', max_tanimoto_thresh)

    @classmethod
    def encode_excluded_mols(cls,
                             excluded_smiles: List[str],
                             pool) -> List[bitarray]:
        cls._excluded_mols = [encoded_cmpd for encoded_cmpd in pool.imap(
            partial(cls._input_fingerprinter.fingerprint_and_encode,
                    encoding='bitarray'),
            excluded_smiles)]

    @classmethod
    def _filter_func(cls, neg_smile: str) -> bool:
        neg_smile_bitarray = cls._input_fingerprinter.fingerprint_and_encode(
            neg_smile, 'bitarray')
        if neg_smile_bitarray is None:
            return False
        for excluded_mol_bitarray in cls._excluded_mols:
            tani = cls._calculate_tanimoto(excluded_mol_bitarray,
                                           neg_smile_bitarray)
            if tani > cls._max_tanimoto_thresh:
                return False
        return True

    @staticmethod
    def _calculate_tanimoto(left_bitarr: bitarray,
                            right_bitarr: bitarray) -> float:
        return ((left_bitarr & right_bitarr).count() /
                (left_bitarr | right_bitarr).count())
