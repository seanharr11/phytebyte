from abc import ABC, abstractmethod
from bitarray import bitarray
import numpy as np
from openbabel import openbabel as ob
from openbabel import pybel
import warnings

from phytebyte.fingerprinters.bitstring_cache_fingerprinter import (
    BitstringCacheFingerprinter)
from .io import PybelDeserializer

warnings.simplefilter("ignore", DeprecationWarning)
# https://www.numpy.org/devdocs/release.html#id19


class PybelFingerprinter(BitstringCacheFingerprinter, PybelDeserializer, ABC):
    def smiles_to_nparray(self, smiles: str):
        fp = self.smiles_to_fingerprint(smiles)
        if fp:
            arr = np.zeros(self._pybel_fp_length, dtype=np.uint8)
            arr[fp.bits] = True
            return arr

    def smiles_to_bitarray(self, smiles: str):
        np_arr = self.smiles_to_nparray(smiles)
        if np_arr is not None:
            return bitarray(list(np_arr))

    def smiles_to_fingerprint(self, smiles: str):
        mol = self.smiles_to_molecule(smiles)
        if mol:
            fp = self._molecule_to_fingerprint(mol)
            return fp

    def smiles_to_molecule(self, smiles: str):
        try:
            mol = pybel.readstring("smi", smiles)
        except Exception as e:
            self.logger.error(e)
            return None
        return mol

    def _molecule_to_fingerprint(self, mol):
        try:
            fp = mol.calcfp(self._pybel_fp_name)
        except ValueError as e:
            self.logger.critical(e)
            self.logger.critical(
                "self._pybel_fp_name should return one of"
                f" {pybel.fps}")
            raise
        return fp

    @property
    @abstractmethod
    def fp_type(self):
        pass

    @property
    @abstractmethod
    def _pybel_fp_name(self):
        pass

    @property
    @abstractmethod
    def _pybel_fp_length(self):
        pass
