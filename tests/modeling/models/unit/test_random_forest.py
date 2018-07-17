import pytest
from unittest.mock import Mock, MagicMock
import numpy as np

from phytebyte.modeling.models.random_forest import (
    RandomForestBinaryClassifierModel)


@pytest.fixture
def nbci():
    nbci = Mock()
    nbci.index = MagicMock(
        return_value=(np.random.randn(10, 10),
                      np.append(
                          np.ones(5), np.zeros(5))))
    return nbci


@pytest.fixture
def rfbcm():
    return RandomForestBinaryClassifierModel()


def test_expected_encoding(rfbcm):
    assert rfbcm.expected_encoding == "numpy"


def test_train(rfbcm, nbci):
    rfbcm.train(nbci, np.arange(5))
    assert rfbcm._rfc


def test_calc_score(rfbcm, nbci):
    rfbcm.train(nbci, np.arange(5))
    score = rfbcm.calc_score(np.append(np.zeros(5), np.ones(5)))
    assert isinstance(score, float)


def test_predict(rfbcm, nbci):
    rfbcm.train(nbci, np.arange(5))
    pred_class = rfbcm.predict(
        np.append(np.zeros(5), np.ones(5)),
        0.5)
    assert pred_class in [0, 1]
