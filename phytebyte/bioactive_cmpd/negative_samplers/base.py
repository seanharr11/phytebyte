from abc import abstractmethod, ABC
from multiprocessing import cpu_count, Pool
import numpy as np
from typing import List, Iterator


from phytebyte.bioactive_cmpd.sources.base import BioactiveCompoundSource
from phytebyte.fingerprinters.base import Fingerprinter


class NotEnoughSamples(Exception):
    pass


class NegativeSampler(ABC):
    def __init__(self,
                 source: BioactiveCompoundSource,
                 fingerprinter: Fingerprinter,
                 num_proc: int=cpu_count(),
                 *args, **kwargs):
        self._source = source
        self._fingerprinter = fingerprinter
        self._num_proc = num_proc
        self._excluded_mol_bitarrays = None

    def sample(self, excluded_smiles_ls: List[str], sz: int) -> Iterator[
                                                                   np.ndarray]:
        rand_neg_smiles_iter = self._source.fetch_random_compounds_exc_smiles(
            excluded_smiles=excluded_smiles_ls,
            limit=sz * 2)
        self._excluded_mol_bitarrays = [
            self._fingerprinter.smiles_to_bitarray(smiles)
            for smiles in excluded_smiles_ls]
        with Pool(self._num_proc) as p:
            cnt = 0
            for neg_ndarray in p.imap_unordered(
               self._filter, rand_neg_smiles_iter):
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

    @abstractmethod
    def _filter(self, smiles: str) -> np.ndarray:
        """ Params: smiles :str - The SMiLES (str) representation of the cmpd
            Returns: np.ndarray representing the Fingerprinter-encoded repr
        """
        pass
