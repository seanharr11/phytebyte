import pytest
from unittest.mock import Mock, MagicMock, PropertyMock
import numpy as np
from bitarray import bitarray

from phytebyte.modeling.input.binary_classifier_input \
        import BitarrayBinaryClassifierInput
from phytebyte.modeling.models.tanimoto import (
    TanimotoBinaryClassifierModel)


@pytest.fixture
def bbci():
    bbci = Mock()
    bbci.index = MagicMock(
        return_value=([bitarray('100')] * 10,
                      np.ones(10)))
    return bbci


@pytest.fixture
def tbcm():
    return TanimotoBinaryClassifierModel()


def test_expected_encoding(tbcm):
    assert tbcm.expected_encoding == "bitarray"


def test_train(tbcm, bbci):
    tbcm.train(bbci, np.arange(5))
    assert tbcm._pos


def test_calc_score(tbcm, bbci):
    tbcm.train(bbci, np.arange(5))
    score = tbcm.calc_score(bitarray('010'))
    assert isinstance(score, float)


def test_predict(tbcm, bbci):
    tbcm.train(bbci, np.arange(5))
    pred_class = tbcm.predict(bitarray('001'), 0.8)
    assert pred_class in [0, 1]
