from abc import abstractmethod, ABC
from multiprocessing import cpu_count, Pool
from typing import List, Iterator

from phytebyte.bioactive_cmpd.sources.base import BioactiveCompoundSource
from phytebyte.fingerprinters.base import Fingerprinter


class NotEnoughSamples(Exception):
    pass


class NegativeSampler(ABC, object):
    output_fingerprinter = None
    output_encoding = None

    def __init__(self,
                 source: BioactiveCompoundSource,
                 fingerprinter: Fingerprinter,
                 num_proc: int=None,
                 *args, **kwargs):
        self._source = source
        self._num_proc = num_proc or cpu_count()
        self._excluded_mol_ls = None

        self.fingerprinter = fingerprinter

    @classmethod
    def create(cls, negative_sampler_name: str,
               source: BioactiveCompoundSource,
               fingerprinter: Fingerprinter,
               *args, **kwargs):
        if negative_sampler_name == 'Tanimoto':
            from .tanimoto_thresh import TanimotoThreshNegativeSampler
            return TanimotoThreshNegativeSampler(
                source, fingerprinter, *args, **kwargs)
        else:
            raise NotImplementedError

    @classmethod
    def set_output_encoding(cls, encoding: str):
        cls._output_encoding = encoding

    def sample(self,
               excluded_positive_smiles_ls: List[str],
               sz: int,
               output_fingerprinter: Fingerprinter) -> Iterator:
        assert self._output_encoding is not None,\
            "Must 'set_output_encoding()' before sampling"
        rand_neg_smiles_iter = self._source.fetch_random_compounds_exc_smiles(
            excluded_smiles=excluded_positive_smiles_ls,
            limit=sz * 2)
        NegativeSampler.output_fingerprinter = output_fingerprinter
        with Pool(processes=self._num_proc) as p:
            self.encode_excluded_mols(excluded_positive_smiles_ls, p)
        with Pool(processes=self._num_proc, initializer=self._init_pool) as p:
            cnt = 0
            for neg_x in p.imap(
               self._filter_and_encode, rand_neg_smiles_iter):
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

    @classmethod
    def _init_pool(cls):
        cls.output_fingerprinter.load_cache()

    @classmethod
    def _filter_and_encode(cls, neg_smiles: str):
        return cls.output_fingerprinter.fingerprint_and_encode(
                neg_smiles, cls._output_encoding)\
            if cls._filter_func(neg_smiles) else None

    @classmethod
    @abstractmethod
    def _filter_func(cls, smiles: str) -> bool:
        """ Params: smiles :str - The SMiLES (str) representation of the cmpd
            Returns: Whether or not to include the SMiLES cmpd as neg sample
        """
        pass

    @classmethod
    @abstractmethod
    def encode_excluded_mols(self, excluded_smiles: List[str]) -> List:
        """ Convert the `excluded_smiles` list into whatever encoding is
        required to be accessed within the concurrent `filter_and_encode`
        step, and it's call to _filter_func()`
        """
        pass
