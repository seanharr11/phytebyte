from abc import ABC, abstractmethod
from bitarray import bitarray
import numpy as np
import pybel

from phytebyte.fingerprinters import Fingerprinter
from .io import PybelDeserializer


class PybelFingerprinter(Fingerprinter, PybelDeserializer, ABC):
    def smiles_to_nparray(self, smiles: str):
        fp = self.smiles_to_fingerprint(smiles)
        if fp:
            arr = np.zeros(self._pybel_fp_length, dtype=np.uint8)
            arr[fp.bits] = True
            return arr

    def smiles_to_bitarray(self, smiles: str):
        fp = self.smiles_to_fingerprint(smiles)
        return bitarray([i in fp.bits for i in range(self._pybel_fp_length)])

    def smiles_to_fingerprint(self, smiles: str):
        mol = self.smiles_to_molecule(smiles)
        if mol:
            fp = self._molecule_to_fingerprint(mol)
            return fp

    def smiles_to_molecule(self, smiles: str):
        try:
            mol = pybel.readstring("smi", smiles)
        except Exception as e:
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
    def _pybel_fp_name(self):
        pass

    @property
    @abstractmethod
    def _pybel_fp_length(self):
        pass
