from abc import ABC, abstractmethod
from typing import Iterator, List

from phytebyte.bioactive_cmpd.types import BioactiveCompound
from phytebyte.fingerprinters.base import Fingerprinter
from .cluster import Cluster


class Clusterer(ABC):
    def __init__(self,
                 fingerprinter: Fingerprinter):
        self._fingerprinter = fingerprinter

    @classmethod
    def create(cls, clusterer_name, fingerprinter,
               *args, **kwargs):
        from .positive_clusterer import PositiveClusterer
        return PositiveClusterer(fingerprinter)

    @abstractmethod
    def find_clusters(self, pos_cmpd_list: List[BioactiveCompound]) -> List[Cluster]:
        pass
