import pytest
from shared import MockFingerprinter, MockBioactiveCmpdSource
from phytebyte.bioactive_cmpd.negative_samplers import (
    TanimotoThreshNegativeSampler)


@pytest.fixture
def output_fingerprinter():
    return MockFingerprinter()


@pytest.fixture
def max_tani_thresh():
    return .6


@pytest.fixture
def ttn_sampler_wo_set_output_encoding(max_tani_thresh):
    mock_fingerprinter = MockFingerprinter()
    mock_bioactive_cmpd_source = MockBioactiveCmpdSource()
    ttn_sampler = TanimotoThreshNegativeSampler(
        mock_bioactive_cmpd_source,
        mock_fingerprinter,
        max_tanimoto_thresh=max_tani_thresh)
    return ttn_sampler


@pytest.fixture
def ttn_sampler(ttn_sampler_wo_set_output_encoding):
    ttn_sampler_wo_set_output_encoding.set_output_encoding('numpy')
    return ttn_sampler_wo_set_output_encoding
