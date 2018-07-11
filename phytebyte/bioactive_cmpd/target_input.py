from abc import abstractmethod, ABC
from typing import List, Iterator

from .sources import BioactiveCompoundSource
from .types import BioactiveCompound


class TargetInput(ABC):

    @abstractmethod
    def fetch_bioactive_cmpds(self, source: BioactiveCompoundSource
                              ) -> Iterator[BioactiveCompound]:
        pass


class PhenotypesTargetInput(TargetInput):
    def __init__(self, phenotypes: List[str]):
        self._phenotypes = phenotypes
        raise NotImplemented

    def fetch_bioactive_cmpds(self, source: BioactiveCompoundSource):
        raise NotImplemented


class GeneTargetsInput(TargetInput):
    def __init__(self, gene_targets: List[str]):
        self._gene_targets = gene_targets

    def fetch_bioactive_cmpds(self, source: BioactiveCompoundSource):
        return source.fetch_with_gene_tgts(self._gene_targets)


class CompoundNamesTargetInput(TargetInput):
    def __init__(self, compound_names: List[str]):
        self._compound_names = compound_names

    def fetch_bioactive_cmpds(self, source: BioactiveCompoundSource):
        return source.fetch_with_compound_names(self._compound_names)


class MetabolitesTargetInput(TargetInput):
    pass
