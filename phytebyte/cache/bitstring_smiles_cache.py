from abc import ABC, abstractmethod
import ujson as json
import os
from typing import List

from phytebyte import ROOT_DIR
from phytebyte.fingerprinters import Fingerprinter


class BitstringSmilesCache(ABC, object):
    @classmethod
    def create(cls, name: str, *args, **kwargs):
        if name == 'json':
            return JsonBitstringSmilesCache(*args, **kwargs)

    @abstractmethod
    def get(smiles: List[str], fp_type: str):
        """ Given a smiles string, a fingerprint type,
        retrieve the fingerprints bitstrng associated with the provided smiles.
        """
        pass

    @abstractmethod
    def update(smiles: List[str], fingerprinter: Fingerprinter):
        # At the moment, doesn't ensure that the fingerprint type associated w/
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


class JsonBitstringSmilesCache(BitstringSmilesCache):
    def __init__(self, fp_type, root_dir=ROOT_DIR):
        self._root_dir = root_dir
        self._fp_type = fp_type
        self._cache = None

    def load(self):
        filename = f'{self._fp_type}.json'
        self._filepath = f'{self._root_dir}/.cache/{filename}'
        print(f"Loading cache from '{self._filepath}'")
        if os.path.exists(self._filepath):
            with open(self._filepath, 'r') as f:
                self._cache = json.load(f)
        else:
            self._cache = {}

    def get(self, smiles):
        return self._cache.get(smiles)

    def update(self, smiles, fingerprinter):
        bitstring = fingerprinter.smiles_to_bitstring(smiles)
        self._cache[smiles] = bitstring

    def write(self):
        print(f"Dumping cache to '{self._filepath}'")
        with open(self._filepath, 'w+') as f:
            json.dump(self._cache, f)

    def clear(self):
        self._cache = {}
