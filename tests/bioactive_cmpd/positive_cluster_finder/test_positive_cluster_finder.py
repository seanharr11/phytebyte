import pytest

from phytebyte.bioactive_cmpd.positive_cluster_finder
from phytebyte.bioactive_cmpd.types import BioactiveCompound


def test_init(pc_finder):
    assert pc_finder.fingerprinter


def test_finder_returns_list(pc_finder):
    my_bc = [BioactiveCompound(1, "", "", "C=N", "", "", "")]
    pos_clusters = pc_finder.find_clusters(my_bc)
    assert isinstance(pos_clusters, list)


def test_finder_returns_list_of_bioactive_cmpds(pc_finder):
    my_bc = [BioactiveCompound(1, "", "", "C=N", "", "", "")]
    pos_clusters = pc_finder.find_clusters(my_bc)
    assert isinstance(pos_clusters[0], BioactiveCompound)
