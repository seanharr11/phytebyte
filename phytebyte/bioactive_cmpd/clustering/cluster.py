from typing import List

from phytebyte.bioactive_cmpd.types import BioactiveCompound
from phytebyte.fingerprinters import Fingerprinter


class Cluster():
    def __init__(self,
                 fingerprinter: Fingerprinter,
                 bioactive_cmpds: BioactiveCompound,
                 *args, **kwargs):
        self._fingerprinter = fingerprinter
        self._bioactive_cmpds = bioactive_cmpds

    @property
    def get_encoded_cmpds(self, encoding: str) -> List:
        return [self._fingerprinter.fingerprint_and_encode(cmpd.smiles)
                for cmpd in self._bioactive_cmpds]

    @property
    def bioactive_cmpds(self) -> List[BioactiveCompound]:
        return self._bioactive_cmpds
