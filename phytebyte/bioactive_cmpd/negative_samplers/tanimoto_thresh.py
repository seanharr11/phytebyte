from bitarray import bitarray
from functools import partial
from typing import List

from .base import NegativeSampler
from phytebyte.fingerprinters import Fingerprinter


class TanimotoThreshNegativeSampler(NegativeSampler):
    _input_fingerprinter = "Foo"
    # If this is never set in __init__ below, the `start_method` is likely "spawn" rather than "fork"
    # https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods
    _max_tanimoto_thresh = None

    def __init__(self,
                 *args,
                 max_tanimoto_thresh=.6,
                 **kwargs):
        setattr(TanimotoThreshNegativeSampler,
                '_max_tanimoto_thresh', max_tanimoto_thresh)
        setattr(TanimotoThreshNegativeSampler,
                '_input_fingerprinter', Fingerprinter.create("daylight"))
        super().__init__(*args, **kwargs)

    @classmethod
    def encode_excluded_mols(cls,
                             excluded_smiles: List[str],
                             pool) -> List[bitarray]:
        if cls._input_fingerprinter is None:
            raise Exception(
                "Despite this being a classmethod, some consumer, somewhere"
                " must instanitate this class before using this method, so"
                " we have an _input_fingerprinter set. Can't mock out a "
                " call from a class attribute in pytest!")
        return [encoded_cmpd for encoded_cmpd in pool.imap(
            partial(cls._input_fingerprinter.fingerprint_and_encode,
                    encoding='bitarray'),
            excluded_smiles)]

    @classmethod
    def _filter_func(cls, neg_smile: str) -> bool:
        neg_smile_bitarray = cls._input_fingerprinter.fingerprint_and_encode(
            neg_smile, 'bitarray')
        if neg_smile_bitarray is None:
            return False
        for excluded_mol_bitarray in cls.excluded_mols:
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
