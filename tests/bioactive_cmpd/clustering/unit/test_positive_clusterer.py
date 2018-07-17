import pytest
from unittest.mock import Mock, MagicMock
import numpy as np

from phytebyte.bioactive_cmpd.clustering.cluster import Cluster
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
    return PositiveClusterer(fingerprinter)


@pytest.fixture
def mock_dbscan():
    # TODO: This isn't used!
    dbs = Mock()
    dbs.labels_ = MagicMock(return_value=[0, 0, 1])
    return dbs


def test_init(pc):
    assert pc._fingerprinter


def test_run_dbscan(pc):
    data = np.zeros((10, 2))
    labels = pc.run_dbscan(100, data)
    assert isinstance(labels, np.ndarray)
    assert len(labels) == data.shape[0]


def test_get_silhouette(pc):
    data = np.zeros((10, 2))
    ss = pc.get_silhouette([0, 1] * 5, data)
    assert isinstance(ss, np.float64)


def test_silhouette_series(pc):
    data = np.zeros((10, 2))
    pc.run_dbscan = MagicMock(return_value=np.zeros(10))
    pc.get_silhouette = MagicMock(return_value=0.2)
    ss_seq = pc.silhouette_series([1, 10, 100], data)
    assert isinstance(ss_seq, np.ndarray)
    assert np.all((ss_seq == -2) |
                  np.logical_and(ss_seq >= -1, ss_seq <= 1))


def test_find_clusters(pc, bc):
    pc.silhouette_series = MagicMock(return_value=np.array([0.1, 0.2, 0.1]))
    assert len(pc.find_clusters([bc])) == 1
    pc.silhouette_series = MagicMock(return_value=np.array([0, 0.1, 0.7]))
    with pytest.raises(Exception):
        pc.find_clusters([bc])
    pc.silhouette_series = MagicMock(return_value=np.array([0.1, 0.7, 0.1]))
    pc.run_dbscan = MagicMock(return_value=np.zeros(10))
    assert isinstance(pc.find_clusters([bc] * 10), list)
    assert all([isinstance(c, Cluster) for c in pc.find_clusters([bc] * 10)])
