from phytebyte.bioactive_cmpd.negative_samplers import (
    NotEnoughSamples)

import pytest
import types


def test_init(ttn_sampler):
    assert ttn_sampler.source
    assert ttn_sampler.fingerprinter


def test_sample_returns_iter(ttn_sampler):
    sample_iter = ttn_sampler.sample(['C=N'], 100)
    assert isinstance(sample_iter, types.GeneratorType)


def test_sample_returns_iter_of_smiles_strs(ttn_sampler):
    sample_iter = ttn_sampler.sample(['C=N'], 100)
    sample = next(sample_iter)
    [_ for _ in sample_iter]
    assert isinstance(sample, str)


def test_sample__sz_is_respected(ttn_sampler):
    samples = [sample for sample in ttn_sampler.sample(['C=N'], 100)]
    assert len(samples) == 100


def test_sample__should_query_for_more_smiles_than_sz(ttn_sampler):
    samples = [sample for sample in ttn_sampler.sample(['C=N'], 100)]
    assert len(samples) == 100
    assert ttn_sampler.source.call_args_ls == [
        (['C=N'], 200,)],\
        "We should query *twice the size"\
        " of our intended neg. samp. size, with the consideration that the DB"\
        " conn should only return chunks of rows, to be iterated over!"\
        " See the call to 'self.source.fetch_random_compounds_exc_smiles()'"


def test_sample__parent_process_does_not_call_smiles_to_bitarray(ttn_sampler):
    # We know _init_proc is called with 'excluded_smiles' = ['C=N']
    sample_iter = ttn_sampler.sample(['C=N'], 100)
    [sample for sample in sample_iter]
    # We expect each process to call 'fingerprinter.smiles_to_bitarray()'
    # len(['C=N']) times, for each process
    cnt = ttn_sampler.fingerprinter.call_arg_ls.count(("C=N",))
    assert cnt == 0


def test_raises_NotEnoughSamples(ttn_sampler):
    sample_iter = ttn_sampler.sample(["CO=N2"]*1000, 1000)
    with pytest.raises(NotEnoughSamples):
        [_ for _ in sample_iter]
