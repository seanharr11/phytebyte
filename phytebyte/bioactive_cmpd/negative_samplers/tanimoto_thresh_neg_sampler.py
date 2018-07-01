from bitarray import bitarray
from multiprocessing import Pool, cpu_count
import numpy as np
from typing import List, Iterator


from phytebyte.bioactive_cmpd.sources.base import BioactiveCompoundSource
from phytebyte.fingerprinters.base import Fingerprinter


class NotEnoughSamples(Exception):
    pass


class TanimotoThreshNegativeSampler():
    def __init__(self,
                 source: BioactiveCompoundSource,
                 fingerprinter: Fingerprinter,
                 max_tanimoto_thresh=.6,
                 num_proc=cpu_count()):
        self._max_tanimoto_thresh = max_tanimoto_thresh
        self._num_proc = num_proc
        self.source = source
        self.fingerprinter = fingerprinter

    def sample(self, excluded_smiles_ls: List[str], sz: int) -> Iterator[str]:
        rand_neg_smiles_iter = self.source.fetch_random_compounds_exc_smiles(
            excluded_smiles=excluded_smiles_ls,
            limit=sz * 2)
        with Pool(self._num_proc,
                  initializer=self._init_proc,
                  initargs=(excluded_smiles_ls,)) as p:
            cnt = 0
            for neg_ndarray in p.imap_unordered(
               self._threshold_on_tanimoto, rand_neg_smiles_iter):
                if neg_ndarray is not None:
                    cnt += 1
                    if cnt > sz:
                        p.terminate()
                        p.join()
                        break
                    yield neg_ndarray
            if cnt < sz:
                p.terminate()
                p.join()
                raise NotEnoughSamples(
                    f"Queried {sz*2} samples, filterd to {cnt}, expected {sz}")

    def _init_proc(self, excluded_smiles: List[str]) -> None:
        global excluded_mol_bitarrays
        excluded_mol_bitarrays = [
            self.fingerprinter.smiles_to_bitarray(smiles)
            for smiles in excluded_smiles]

    def _threshold_on_tanimoto(self, neg_smile: str) -> np.ndarray:
        neg_smile_bitarray = self.fingerprinter.smiles_to_bitarray(neg_smile)
        for excluded_mol_bitarray in excluded_mol_bitarrays:
            tani = self._calculate_tanimoto(excluded_mol_bitarray,
                                            neg_smile_bitarray)
            if tani > self._max_tanimoto_thresh:
                return None
        return self.fingerprinter.bitarray_to_nparray(neg_smile_bitarray)

    @staticmethod
    def _calculate_tanimoto(left_bitarr: bitarray,
                            right_bitarr: bitarray) -> float:
        return ((left_bitarr & right_bitarr).count() /
                (left_bitarr | right_bitarr).count())
