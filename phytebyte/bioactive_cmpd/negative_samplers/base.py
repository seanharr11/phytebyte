from abc import abstractmethod, ABC
from multiprocessing import cpu_count, Pool
from typing import List, Iterator

from phytebyte.bioactive_cmpd.sources.base import BioactiveCompoundSource
from phytebyte.fingerprinters.base import Fingerprinter


class NotEnoughSamples(Exception):
    pass


class NegativeSampler(ABC):
    def __init__(self,
                 source: BioactiveCompoundSource,
                 fingerprinter: Fingerprinter,
                 neg_sample_encoding: str,
                 num_proc: int=cpu_count(),
                 *args, **kwargs):
        self._source = source
        self._fingerprinter = fingerprinter
        self._neg_sample_encoding = neg_sample_encoding
        self._num_proc = num_proc
        self._excluded_mol_ls = None

    def sample(self, excluded_smiles_ls: List[str], sz: int) -> Iterator:
        rand_neg_smiles_iter = self._source.fetch_random_compounds_exc_smiles(
            excluded_smiles=excluded_smiles_ls,
            limit=sz * 2)
        self._excluded_mol_ls = self._encode_excluded_mol_ls(
            excluded_smiles_ls)
        with Pool(self._num_proc) as p:
            cnt = 0
            for neg_x in p.imap_unordered(
               self._filter_and_convert, rand_neg_smiles_iter):
                if neg_x is not None:
                    cnt += 1
                    if cnt > sz:
                        p.terminate()
                        p.join()
                        break
                    yield neg_x
            if cnt < sz:
                p.terminate()
                p.join()
                raise NotEnoughSamples(
                    f"Queried {sz*2} samples, filterd to {cnt}, expected {sz}")

    def _filter_and_encode(self, neg_smiles: str):
        return self.dispatched_fp_encoding_func(neg_smiles)\
            if self._filter_func(neg_smiles) else None

    # TODO: @lazy_property
    def _dispatched_fp_encoding_func(self, encoding: str):
        if encoding == 'numpy':
            return self._fingerprinter.smiles_to_nparray
        elif encoding == 'bitarray':
            return self._fingerprinter.smiles_to_bitarray
        else:
            raise NotImplementedError

    @abstractmethod
    def _filter_func(self, smiles: str) -> bool:
        """ Params: smiles :str - The SMiLES (str) representation of the cmpd
            Returns: Whether or not to include the SMiLES cmpd as neg sample
        """
        pass

    @abstractmethod
    def _encode_excluded_mol_ls(self, excluded_smiles: List[str]) -> List:
        """ Convert the `excluded_smiles` list into whatever encoding is
        required to be accessed within the concurrent `filter_and_encode`
        step, and it's call to _filter_func()`
        """
        pass
