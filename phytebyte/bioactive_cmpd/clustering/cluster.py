from typing import List

from phytebyte.bioactive_cmpd.types import BioactiveCompound
from phytebyte.fingerprinters import Fingerprinter


class Cluster():
    def __init__(self,
                 bioactive_cmpds: BioactiveCompound,
                 *args,
                 **kwargs):
        self._bioactive_cmpds = bioactive_cmpds

    def get_encoded_cmpds(self, encoding: str,
                          fingerprinter: Fingerprinter) -> List:
        return [fingerprinter.fingerprint_and_encode(cmpd.smiles, encoding)
                for cmpd in self._bioactive_cmpds]

    @property
    def bioactive_cmpds(self) -> List[BioactiveCompound]:
        return self._bioactive_cmpds
