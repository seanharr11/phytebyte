from unittest.mock import MagicMock, Mock
import pytest

from shared import MockFingerprinter, MockBioactiveCmpdSource
from phytebyte.bioactive_cmpd.negative_samplers import (
    TanimotoThreshNegativeSampler)


@pytest.fixture
def output_fingerprinter():
    return MockFingerprinter()


@pytest.fixture
def input_fingerprinter():
    return MockFingerprinter()


@pytest.fixture
def max_tani_thresh():
    return .6


@pytest.fixture
def ttn_sampler(output_fingerprinter, input_fingerprinter,
                max_tani_thresh, monkeypatch):
    mock_bioactive_cmpd_source = MockBioactiveCmpdSource()
    mock_fingerprinter_factory = Mock()
    mock_fingerprinter_factory.create = MagicMock(
        return_value=input_fingerprinter)
    monkeypatch.setattr(
        "phytebyte.bioactive_cmpd.negative_samplers"
        ".tanimoto_thresh.Fingerprinter", mock_fingerprinter_factory)
    ttn_sampler = TanimotoThreshNegativeSampler(
        mock_bioactive_cmpd_source,
        max_tanimoto_thresh=max_tani_thresh)

    return ttn_sampler
