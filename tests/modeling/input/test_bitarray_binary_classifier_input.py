import pytest
import numpy as np
from bitarray import bitarray
from typing import List

from phytebyte.modeling.input \
    .binary_classifier_input import \
    BitarrayBinaryClassifierInput


@pytest.fixture
def pos():
    return [bitarray('001') for _ in range(10)]


@pytest.fixture
def neg():
    return [bitarray('001') for _ in range(10)]


def test_init(pos, neg):
    bbci = BitarrayBinaryClassifierInput(pos, neg)
    assert isinstance(bbci._X, list)
    assert len(bbci._X) == len(pos) + len(neg)


@pytest.fixture
def bbci(pos, neg):
    return BitarrayBinaryClassifierInput(pos, neg)


def test__len__(bbci):
    assert len(bbci) == 20


def test_index(bbci):
    subset = np.array([5, 15])
    X, y = bbci.index(subset)
    assert isinstance(X, list)
    assert len(X) == 2
