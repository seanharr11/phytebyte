import pytest
import numpy as np

from phytebyte.modeling.input \
    .binary_classifier_input import \
    NumpyBinaryClassifierInput

@pytest.fixture
def pos():
    return np.zeros((10, 10))


@pytest.fixture
def neg():
    return np.zeros((10, 10))


def test_init(pos, neg):
    nbci = NumpyBinaryClassifierInput(pos, neg)
    assert isinstance(nbci._X, np.ndarray)
    assert len(nbci._X) == len(pos) + len(neg)


@pytest.fixture
def nbci(pos, neg):
    return NumpyBinaryClassifierInput(pos, neg)


def test__len__(nbci):
    assert len(nbci) == 20


def test_index(nbci):
    subset = np.array([5,15])
    X, y = nbci.index(subset)
    assert isinstance(X, np.ndarray)
    assert len(X) == 2
