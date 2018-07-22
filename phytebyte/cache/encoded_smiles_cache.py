from abc import ABC, abstractmethod
import pickle
from typing import List

from phytebyte import ROOT_DIR
from phytebyte.fingerprinters import Fingerprinter

    
class EncodedSmilesCache(ABC, object):
    @abstractmethod
    def __init__(self, fp_type: str, encoding: str):
        """ Given a fingerprint type and a requested encoding, store these
        specifications as attributes and 'load' the proper database (in memory, as
        a Python object, etc.).
        """
        pass

    @abstractmethod
    def get(smiles: List[str], fp_type: str, encoding: str):
        """ Given a smiles string, a fingerprint type, and a request encoding, retrieve
        the fingerprints encoding associated with the provided smiles.
        """
        pass

    @abstractmethod
    def update(smiles: List[str], fingerprinter: Fingerprinter):
        # At the moment, doesn't ensure that the fingerprint type associated with
        # the fingerprinter and the cache class are the same.
        """ Given a smiles string and a fingerprinter, generate the encoding and
        store it in the relevant data object or database.
        """
        pass

    @abstractmethod
    def write():
        """ Some cache types (e.g. Python objects) may need to be explicitly
        written after being updated, while others (e.g. databases) may not. If
        needed, write the file here, otherwise pass.
        """
        pass

    @abstractmethod
    def clear():
        """ Clear the current cache. """
        pass


class DictEncodedSmilesCache(EncodedSmilesCache):
    def __init__(self, fp_type, encoding, root_dir=ROOT_DIR):
        self.fp_type = fp_type
        self.encoding = encoding
        self._filepath = f'{root_dir}/.cache/{fp_type}_{encoding}.pkl'
        with open(self._filepath, 'rb') as f:
            self._cache = pickle.load(f)

    def get(self, smiles):
        return self._cache[smiles]

    def update(self, smiles, fingerprinter):
        encoded_smiles = fingerprinter.fingerprint_and_encode(smiles,
                                                              self.encoding)
        self._cache[smiles] = encoded_smiles

    def write(self):
        with open(self._filepath, 'wb') as f:
            pickle.dump(self._cache, f)

    def clear(self):
        self._cache = {}
        # Should this method also delete the system file containing the pickled
        # object?
