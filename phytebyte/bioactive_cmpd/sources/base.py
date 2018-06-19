from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from typing import List, Iterator, Callable

from phytebyte.bioactive_cmpd.types import BioactiveCompound


class BioactiveCompoundSource(ABC):
    def __init__(self, db_url):
        engine = create_engine(db_url)
        self.conn = engine.connect()

    @abstractmethod
    def fetch_with_gene_tgts(self, gene_tgts: List[str]) -> \
            Iterator[Callable[[], BioactiveCompound]]:
        """
        Fetch `BioactiveCompounds`, with assayed bioactivity,
        that target specific genes.

        `gene_tgts`: List of strings representing genes. Each
        `BioactiveCompound` returned should target one of the genes in the list
        """
        pass

    @abstractmethod
    def fetch_with_compound_names(self, compound_names: List[str]) -> \
            Iterator[Callable[[], BioactiveCompound]]:
        """
        Fetch `BioactiveCompounds` that have names given by `compound_names`.

        `compound_names`: A list of str's representing the `pref_name` of the
        drugs that should be queried.

        Returns: An iterator of partials, each of which, when called, will
        return a BioactiveCompound. This allows multiple processes to
        deserialize in parallel, rather than a single process deserializing.
        """
        pass

    @abstractmethod
    def fetch_random_compounds_exc_smiles(self, excluded_smiles: List[str],
                                          limit: int) -> Iterator[str]:
        """ Fetch Iterator of SMiLES strs of random compounds, where each
        compound does NOT have its SMiLE string in the `excluded_smiles`
        parameter.

        `excluded_smiles`: List of strings represneting compounds which should
        be excluded from the query.
        `limit`: Number of random `smiles` to fetch.

        Returns: An `Iterator` of str's representing each random compounds'
        SMiLES representation."""
        pass
