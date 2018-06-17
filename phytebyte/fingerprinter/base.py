from abc import ABC, abstractmethod
import bitarray
import numpy as np
from typings import List


class Fingerprinter(ABC):
    """ A 'Fingerprinter' is responsible for translating between different
    molecule representations. Factory method 'create()' instantiates each
    Fingerprinter implementation.
    """
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def create(cls, fingerprint_name, *args, **kwargs) -> 'Fingerprinter':
        """ Factory method to allow easy creation of Fingerprinter objects """
        fp_class = cls._available_fingerprints.get(
            fingerprint_name)
        if fp_class is None:
            raise Exception(
                f"Can't support fingerprint_name: '{fingerprint_name}'"
                f"\n --> Choices: {list(cls._available_fingerprints.keys())}")
        return fp_class(*args, **kwargs)

    def smiles_to_nparrays(self, smiles_iter) -> np.ndarray:
        """ Converts `smiles_iter` into an np.array of np.arrays,
        with each fingerprint being encoded as an np.array of dtype uint8,
        each of which holds 0's and 1's.
        """
        return np.array(
            [self._smiles_to_nparray(smiles) for smiles in smiles_iter])

    def smiles_to_bitarrays(self, smiles_iter) -> List[bitarray]:
        """ Converts `smiles_iter` into a List of bitarrays - a low-level
        C-implementation of a bitarray, exposed to Python via library"""
        return [bitarray(list(self._smiles_to_nparray(smiles))
                for smiles in smiles_iter)]

    def bitarrays_to_nparrays(self, bitarray_iter) -> np.ndarray:
        """ Converts bitarray encoding of each Fingerprint into an nparray  """
        return [np.array(bitarray.tolist()) for bitarray in bitarray_iter]

    @abstractmethod
    def smiles_to_nparray(self, smiles: str) -> np.array:
        pass

    @abstractmethod
    def smiles_to_bitarray(self, smiles: str) -> bitarray:
        pass

    @classmethod
    def _available_fingerprints(cls):
        from .daylight import (DaylightFingerprinter)
        return {
                'daylight': DaylightFingerprinter
        }
