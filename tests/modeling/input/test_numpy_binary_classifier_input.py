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
    assert nbci


@pytest.fixture
def nbci(pos, neg):
    return NumpyBinaryClassifierInput(pos, neg)

def test_split(nbci):
    nbci.split()
    assert len(nbci._train_idx) == 14
    assert len(nbci._test_idx) == 6


def test_train(nbci):
    nbci._train_idx = np.arange(14)
    X_train, y_train = nbci.train
    assert isinstance(X_train, np.ndarray)
    assert isinstance(y_train, np.ndarray)
    assert len(X_train) == 14
    assert len(y_train) == 14


def test_test(nbci):
    nbci._test_idx = np.arange(14, 20)
    X_test, y_test = nbci.test
    assert isinstance(X_test, np.ndarray)
    assert isinstance(y_test, np.ndarray)
    assert len(X_test) == 6
    assert len(y_test) == 6
