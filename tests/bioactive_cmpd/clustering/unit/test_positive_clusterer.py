import pytest
from unittest.mock import Mock, MagicMock
import numpy as np

from phytebyte.bioactive_cmpd.clustering.positive_clusterer import (
    PositiveClusterer)
from phytebyte.bioactive_cmpd.types import BioactiveCompound


class MockFingerprinter(object):
    smile_to_fp_dict = {
        "C=N": [0, 1] * 512
    }

    def __init__(self):
        pass

    def smiles_to_nparray(self, smiles):
        fp = self.smile_to_fp_dict[smiles]
        return np.array(fp)

    def smiles_to_nparrays(self, smiles):
        return [self.smiles_to_nparray(s) for s in smiles]


@pytest.fixture
def bc():
    return BioactiveCompound(1, "", "C=N", "", "", "")


@pytest.fixture
def pc(bc):
    fingerprinter = MockFingerprinter()
    return PositiveClusterer([bc], fingerprinter)


@pytest.fixture
def mock_dbscan():
    # TODO: This isn't used!
    dbs = Mock()
    dbs.labels_ = MagicMock(return_value=[0, 0, 1])
    return dbs


def test_init(pc):
    assert pc._pos_cmpds
    assert pc._fingerprinter
    assert pc._data
    assert isinstance(pc._data[0], np.ndarray)


def test_run_dbscan(pc):
    pc._data = np.zeros((10, 2))
    labels = pc.run_dbscan(100)
    assert isinstance(labels, np.ndarray)
    assert len(labels) == pc._data.shape[0]


def test_get_silhouette(pc):
    pc._data = np.zeros((10, 2))
    ss = pc.get_silhouette([0, 1] * 5)
    assert isinstance(ss, np.float64)


def test_silhouette_series(pc):
    pc._data = np.zeros((10, 2))
    pc.run_dbscan = MagicMock(return_value=np.zeros(10))
    pc.get_silhouette = MagicMock(return_value=0.2)
    ss_seq = pc.silhouette_series([1, 10, 100])
    assert isinstance(ss_seq, np.ndarray)
    assert np.all((ss_seq == -2) |
                  np.logical_and(ss_seq >= -1, ss_seq <= 1))


def find_clusters(pc):
    pc.silhouette_series = MagicMock(return_value=[0.1, 0.2, 0.1])
    assert len(pc.find_clusters()) == 1
    pc.silhouette_series = MagicMock(return_value=[0, 0.1, 0.2])
    with pytest.raises(Exception):
        pc.find_clusters()
    pc.silhouette_series = MagicMock(return_value=[0.1, 0.7, 0.1])
    pc._data = np.zeros((10, 2))
    pc.run_dbscan = MagicMock(return_value=np.zeros(10))
    assert len(pc.find_clusters()) == len(pc.silhouette_series())


# def test_finder_returns_list(pc):
#    pos_clusters = pc.find_clusters()
#    assert isinstance(pos_clusters, list)


# def test_finder_returns_list_of_bioactive_cmpds(pc):
#    pos_clusters = pc.find_clusters()
#    # print(type(pos_clusters[0]), type(pos_clusters[0][0]))
#    assert isinstance(pos_clusters[0], list)
#    assert isinstance(pos_clusters[0][0], BioactiveCompound)
