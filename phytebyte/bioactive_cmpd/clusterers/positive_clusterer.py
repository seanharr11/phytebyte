from typing import List

from phytebyte.bioactive_cmpd.types import BioactiveCompound
from phytebyte.fingerprinters.base import Fingerprinter


class PositiveClusterer():
    def __init__(self,
                 pos_cmpds: List[BioactiveCompound],
                 fingerprinter: Fingerprinter):
        self._pos_cmpds = pos_cmpds
        self._fingerprinter = fingerprinter

    def find_clusters(self):
        # pos_dataset = self._fingerprinter.smiles_to_nparrays(
        #     [c.canonical_smiles for c in self._pos_cmpds])
        # No need to create this dataset until "real" implementation
        return [self._pos_cmpds]
        # For now, a list of length one containing the full list of input
        # biaoctive compounds
