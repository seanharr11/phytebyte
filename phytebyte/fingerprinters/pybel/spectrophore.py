import pybel
import numpy as np

from phytebyte.fingerprinters.pybel import PybelDeserializer
from phytebyte.fingerprinters.base import Fingerprinter


class SpectrophoreFingerprinter(Fingerprinter, PybelDeserializer):
    @property
    def fp_type(self) -> str:
        return "spectrophore"

    def __init__(self):
        self._ob_spectrophore = pybel.ob.OBSpectrophore()

    def smiles_to_nparray(self, smiles: str):
        mol = self.smiles_to_molecule(smiles)
        # ^Inherited from PybelDeserializer
        if not mol:
            return None
        mol.make3D()
        ob_mol = mol.OBMol
        spect = self._ob_spectrophore.GetSpectrophore(ob_mol)
        if len(spect) != 48:
            # Sometimes spectrophore FPs can return the wrong shaped np arrays
            # This jacks up our model w/ runtime errors
            # Solution: return None, as these will be filtered out
            return None
        spect_arr = np.nan_to_num(np.array(spect))
        return spect_arr

    def smiles_to_bitarray(self, smiles: str):
        raise NotImplementedError
