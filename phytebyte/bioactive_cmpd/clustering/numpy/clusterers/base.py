from abc import ABC, abstractmethod
from typing import Iterable

from phytebyte.bioactive_cmpd.types import BioactiveCompound
from phytebyte.fingerprinters.base import Fingerprinter
from phytebyte.bioactive_cmpd.clusters import NumpyCluster


class NumpyClusterer(ABC):
    def __init__(self,
                 pos_cmpds: Iterable[BioactiveCompound],
                 fingerprinter: Fingerprinter):
        self._pos_cmpds = pos_cmpds
        self._fingerprinter = fingerprinter

    @abstractmethod
    def find_clusters(self) -> Iterable[NumpyCluster]:
        pass
