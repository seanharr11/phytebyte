from abc import ABC, abstractmethod
from bitarray import bitarray
import numpy as np
import pybel
import warnings

from phytebyte.fingerprinters import Fingerprinter
from .io import PybelDeserializer

warnings.simplefilter("ignore", DeprecationWarning)
# https://www.numpy.org/devdocs/release.html#id19


class PybelFingerprinter(Fingerprinter, PybelDeserializer, ABC):
    @staticmethod
    def nparray_to_bitstring(nparray: np.ndarray):
        if nparray is not None:
            return "".join([str(bit) for bit in list(nparray)])

    @staticmethod
    def bitarray_to_bitstring(bitarr: bitarray):
        if bitarr:
            return str(bitarr)

    @staticmethod
    def bitstring_to_nparray(bitstring: str):
        if bitstring:
            # Add " sep='' " kwarg
            return np.fromstring(bitstring, dtype='uint8')

    @staticmethod
    def bitstring_to_bitarray(bitstring: str):
        if bitstring:
            return bitarray(bitstring)

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
