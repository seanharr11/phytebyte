from abc import ABC, abstractmethod
from bitarray import bitarray
import numpy as np
from typing import List


class Fingerprinter(ABC, object):
    """ A 'Fingerprinter' is responsible for converting serialized compound
    representations (like SMiLES str's), to deserialized Fingerprint objects
    (i.e. Daylight Fingerprint), and finally returning a stripped-down
    representation of these objects for performance (i.e. numpy.array).

    Factory method 'create()' instantiates each Fingerprinter implementation.
    """

    def __init__(self, cache=None, *args, **kwargs):
        self._cache = cache

    @classmethod
    def create(cls, fingerprint_name, cache=None, *args, **kwargs) -> 'Fingerprinter':
        """ Factory method to allow easy creation of Fingerprinter objects """
        available_fps = cls.get_available_fingerprints()
        fp_class = available_fps.get(fingerprint_name)
        if fp_class is None:
            raise Exception(
                f"Can't support fingerprint_name: '{fingerprint_name}'"
                f"\n --> Choices: {list(cls._available_fingerprints.keys())}")
        return fp_class(cache=cache, *args, **kwargs)

    def fingerprint_and_encode(self, smiles: str, encoding: str,
                               use_cache=True):
        if use_cache and self._cache is not None:
            cached_encoding = self._cache.get(smiles, self.fp_type, encoding)
            return cached_encoding if cached_encoding is not None else (
                self.fingerprint_and_encode(smiles, encoding, use_cache=False))
        elif encoding == 'numpy':
            return self.smiles_to_nparray(smiles)
        elif encoding == 'bitarray':
            return self.smiles_to_bitarray(smiles)
        else:
            raise NotImplementedError(encoding)

    def smiles_to_nparrays(self, smiles_iter) -> np.ndarray:
        """ Converts `smiles_iter` into an np.array of np.arrays,
        with each fingerprint being encoded as an np.array of dtype uint8,
        each of which holds 0's and 1's.
        """
        assert type(smiles_iter) is not str,\
            "`smiles_iter` must be a seq of smile strings not single SMiLE str"
        return np.array(
            [self.smiles_to_nparray(smiles) for smiles in smiles_iter])

    def smiles_to_bitarrays(self, smiles_iter) -> List[bitarray]:
        """ Converts `smiles_iter` into a List of bitarrays - a low-level
        C-implementation of a bitarray, exposed to Python via library"""
        assert type(smiles_iter) is not str,\
            "`smiles_iter` must be a seq of smile strings not single SMiLE str"
        return [self.smiles_to_bitarray(smiles)
                for smiles in smiles_iter]

    def bitarrays_to_nparrays(self, bitarray_iter) -> np.ndarray:
        """ Converts bitarray encoding of each Fingerprint into an nparray  """
        return [self.bitarray_to_nparray(bitarr) for bitarr in bitarray_iter]

    def bitarray_to_nparray(self, bitarr) -> np.array:
        """ Converts bitarray encoding of 1 Fingerprint into an nparray  """
        return np.array(bitarr.tolist())

    @abstractmethod
    def smiles_to_nparray(self, smiles: str) -> np.array:
        pass

    @abstractmethod
    def smiles_to_bitarray(self, smiles: str) -> bitarray:
        pass

    @property
    @abstractmethod
    def fp_type(self) -> str:
        """ Returns a string describing the fingerprint type (e.g. 'daylight').
        """
        pass

    @classmethod
    def get_available_fingerprints(cls):
        from phytebyte.fingerprinters.pybel import (
            DaylightFingerprinter, SpectrophoreFingerprinter)
        return {
                'daylight': DaylightFingerprinter,
                'spectrophore': SpectrophoreFingerprinter
        }
