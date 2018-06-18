import pybel
import numpy as np

from phytebyte.fingerprinters.pybel import PybelDeserializer
from .base import Fingerprinter


class SpectrophoreFingerprinter(Fingerprinter, PybelDeserializer):
    def __init__(self):
        self._ob_spectrophore = pybel.ob.OBSpectrophore()

    def smiles_to_nparray(self, smiles: str):
        mol = self.smiles_to_molecule(smiles)
        # ^Inherited from PybelDeserializer
        ob_mol = mol.OBMol
        spect = self._ob_spectrophore.GetSpectrophore(ob_mol)
        return np.array(spect)

    def smiles_to_bitarray(self, smiles: str):
        raise NotImplementedError
