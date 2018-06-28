import sys
# Stress tests


def test_sample__1000(ttn_sampler):
    sample_iter = ttn_sampler.sample(['C=N']*1000, 1000)
    assert len([sample for sample in sample_iter]) == 1000


def test_sample__10000(ttn_sampler):
    sample_iter = ttn_sampler.sample(['C=N']*1000, 10000)
    assert len([sample for sample in sample_iter]) == 10000


def test_sample__100000(ttn_sampler):
    sample_iter = ttn_sampler.sample(['C=N']*1000, 100000)
    assert len([sample for sample in sample_iter]) == 100000


def test_sample__memory_overhead(ttn_sampler):
    sample_iter = ttn_sampler.sample(['C=N']*1000, 1000000)
    samples = [sample for sample in sample_iter]
    size = sys.getsizeof(samples) / 1024 / 1024 / 1024.0
    print(f"Size: {size}")
    assert size < 1.0
