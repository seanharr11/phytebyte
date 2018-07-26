from phytebyte.bioactive_cmpd.negative_samplers import (
    NotEnoughSamples)

import numpy as np
import pytest
import types


def test_init(ttn_sampler):
    assert ttn_sampler._source
    assert ttn_sampler._fingerprinter


def test_sample_wo_set_sample_encoding(ttn_sampler_wo_set_sample_encoding,
                                       output_fingerprinter):
    sample_iter = ttn_sampler_wo_set_sample_encoding.sample(
        ['C=N'], 100, output_fingerprinter)
    with pytest.raises(Exception):
        next(sample_iter)


def test_sample_returns_iter(ttn_sampler,
                             output_fingerprinter):
    sample_iter = ttn_sampler.sample(['C=N'], 100, output_fingerprinter)
    assert isinstance(sample_iter, types.GeneratorType)


def test_sample_returns_iter_of_smiles_ndarrays(ttn_sampler,
                                                output_fingerprinter):
    sample_iter = ttn_sampler.sample(['C=N'], 100, output_fingerprinter)
    sample = next(sample_iter)
    [_ for _ in sample_iter]
    assert isinstance(sample, np.ndarray)


def test_sample__sz_is_respected(ttn_sampler, output_fingerprinter):
    samples = [sample for sample in ttn_sampler.sample(
                  ['C=N'], 100, output_fingerprinter)]
    assert len(samples) == 100


def test_sample__should_query_for_more_smiles_than_sz(
        ttn_sampler, output_fingerprinter):
    samples = [sample for sample in ttn_sampler.sample(
        ['C=N'], 100, output_fingerprinter)]
    assert len(samples) == 100
    assert ttn_sampler._source.call_args_ls == [
        (['C=N'], 200,)],\
        "We should query *twice the size"\
        " of our intended neg. samp. size, with the consideration that the DB"\
        " conn should only return chunks of rows, to be iterated over!"\
        " See the call to 'self._source.fetch_random_compounds_exc_smiles()'"


def test_raises_NotEnoughSamples(ttn_sampler, output_fingerprinter):
    sample_iter = ttn_sampler.sample(["CO=N2"]*1000, 1000,
                                     output_fingerprinter)
    with pytest.raises(NotEnoughSamples):
        [_ for _ in sample_iter]
