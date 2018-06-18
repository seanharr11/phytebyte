from abc import ABC, abstractmethod
from bitarray import bitarray
import numpy as np
import pybel

from phytebyte.fingerprinters import Fingerprinter
from .io import PybelDeserializer


class PybelFingerprinter(Fingerprinter, PybelDeserializer, ABC):
    def smiles_to_nparray(self, smiles: str):
        fp = self.smiles_to_fingerprint(smiles)
        arr = np.zeros(len(fp.bits), dtype=np.uint8)
        arr[fp.bits] = True
        return arr

    def smiles_to_bitarray(self, smiles: str):
        fp = self.smiles_to_fingerprint(smiles)
        return bitarray(fp.bits)

    def smiles_to_fingerprint(self, smiles: str):
        mol = self.smiles_to_molecule(smiles)
        fp = self._molecule_to_fingerprint(mol)
        return fp

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
