import pytest
import numpy as np
from unittest.mock import Mock, MagicMock, PropertyMock
from bitarray import bitarray

from phytebyte.modeling.input.binary_classifier_input \
        import BitarrayBinaryClassifierInput
from phytebyte.modeling.models.tanimoto import (
    TanimotoBinaryClassifierModel)


class MockBBCI(BitarrayBinaryClassifierInput):
    @property
    def train(self):
        return ([bitarray([0] * 10) for _ in range(10)],
                np.ones(10))

    @property
    def test(self):
        return ([bitarray([0] * 10) for _ in range(5)],
                np.ones(5))


@pytest.fixture
def bbci():
    return MockBBCI(np.array([0, 0]), np.array([0, 0]))

def test_train(bbci):
    tbcm = TanimotoBinaryClassifierModel()
    tbcm.train(bbci)
    assert isinstance(tbcm._pos[0], bitarray)
    assert len(tbcm._pos) == 10


def test_predict(bbci):
    tbcm = TanimotoBinaryClassifierModel()
    tbcm.train(bbci)
    pred = tbcm.predict(bitarray([1] * 10))
    assert pred in [0,1]


def test_expected_encoding():
    tbcm = TanimotoBinaryClassifierModel()
    assert tbcm.expected_encoding == "bitarray"


def test_f1(bbci):
    tbcm = TanimotoBinaryClassifierModel()
    with pytest.raises(Exception):
        tbcm.f1()
    tbcm.train()
    tbcm._pos = 1
    f_score = tbcm.f1()
    print(type(f_score))
    #assert isinstance(f_score, 
