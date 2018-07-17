import pytest
from unittest.mock import Mock, MagicMock
import numpy as np

from phytebyte.modeling.models.binary_classifier import (
    BinaryClassifierModel)


@pytest.fixture
def nbci():
    nbci = Mock()
    nbci.__len__ = MagicMock(return_value=10)
    nbci.index = MagicMock(
        return_value=(np.random.randn(10, 10),
                      np.ones(10)))
    return nbci


class MockBCM(BinaryClassifierModel):
    def expected_encoding(self):
        return "abc"

    def train(self, bci, idx):
        return Mock()

    def calc_score(self, encoded_cmpd):
        return 0.7


def test_predict():
    mock_bcm = MockBCM()
    mock_bcm.predict(np.zeros((1, 10)), 0.5)


def test_evaluate(nbci):
    mock_bcm = MockBCM()
    f_score = mock_bcm.evaluate(nbci, 0.5)
    assert f_score
