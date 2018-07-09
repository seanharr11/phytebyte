import pytest
from unittest.mock import Mock, MagicMock

from phytebyte.bioactive_cmpd import ModelDataLoader


@pytest.fixture
def mock_source():
    m = Mock()
    return m


@pytest.fixture
def mock_negative_sampler():
    m = Mock()
    return m


@pytest.fixture
def mock_positive_clusterer():
    m = Mock()
    return m


@pytest.fixture
def mock_target_input():
    m = Mock()
    return m


def test_init(mock_source, mock_negative_sampler,
              mock_positive_clusterer, mock_target_input):
    mdl = ModelDataLoader(mock_source, mock_negative_sampler,
                          mock_positive_clusterer, mock_target_input)
    assert mdl is not None

