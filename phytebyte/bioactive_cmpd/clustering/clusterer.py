from abc import ABC, abstractmethod
from typing import Iterator, List

from phytebyte.bioactive_cmpd.types import BioactiveCompound
from phytebyte.fingerprinters.base import Fingerprinter
from .cluster import Cluster


class Clusterer(ABC):
    def __init__(self,
                 pos_cmpd_iter: Iterator[BioactiveCompound],
                 fingerprinter: Fingerprinter):
        self._pos_cmpd_iter = pos_cmpd_iter
        self._fingerprinter = fingerprinter

    @abstractmethod
    def find_clusters(self) -> List[Cluster]:
        pass
