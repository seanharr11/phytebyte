import bitarray
import numpy as np
import pybel

from .base import Fingerprinter


class DaylightFingerprinter(Fingerprinter):
    def smiles_to_nparray(self, smiles: str):
        fp = self._smiles_to_fingerprint(smiles)
        arr = np.zeroes(1024, dtype=np.uint8)
        arr[fp.bits] = True
        return arr

    def smiles_to_bitarray(self, smiles: str):
        fp = self._smiles_to_fingerprint(smiles)
        return bitarray(fp.bits)

    def _smiles_to_fingerprint(self, smiles: str):
        molecule = pybel.readstring("smi", smiles)
        return molecule.calcfp()
