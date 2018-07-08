import pytest

from phytebyte.bioactive_cmpd.clusterers.positive_clusterer import (
    PositiveClusterer)
from phytebyte.bioactive_cmpd.types import BioactiveCompound


class MockFingerprinter(object):
    smile_to_fp_dict = {
        "C=N": [0,1] * 512
    }

    def __init__(self):
        pass

    def smiles_to_nparray(self, smiles):
        fp = smile_to_fp_dict[smiles]
        return np.array(fp)

    def smiles_to_nparrays(self, smiles):
        return [smiles_to_nparray(s) for s in smiles]


@pytest.fixture
def bc():
    return BioactiveCompound(1, "", "C=N", "", "", "")


@pytest.fixture
def pc(bc):
    fingerprinter = MockFingerprinter()
    return PositiveClusterer([bc], fingerprinter)


def test_init(pc):
    assert pc._fingerprinter


def test_finder_returns_list(pc):
    pos_clusters = pc.find_clusters()
    assert isinstance(pos_clusters, list)


def test_finder_returns_list_of_bioactive_cmpds(pc):
    pos_clusters = pc.find_clusters()
    print(type(pos_clusters[0]), type(pos_clusters[0][0]))
    assert isinstance(pos_clusters[0], list)
    assert isinstance(pos_clusters[0][0], BioactiveCompound)
