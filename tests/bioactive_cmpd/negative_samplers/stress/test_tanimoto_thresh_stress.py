import sys
# Stress tests


def test_sample__1000(ttn_sampler, output_fingerprinter):
    sample_iter = ttn_sampler.sample(['C=N']*1000, 1000,
                                     output_fingerprinter)
    assert len([sample for sample in sample_iter]) == 1000


def test_sample__10000(ttn_sampler, output_fingerprinter):
    sample_iter = ttn_sampler.sample(['C=N']*1000, 10000,
                                     output_fingerprinter)
    assert len([sample for sample in sample_iter]) == 10000


def test_sample__100000(ttn_sampler, output_fingerprinter):
    sample_iter = ttn_sampler.sample(['C=N']*1000, 100000,
                                     output_fingerprinter)
    assert len([sample for sample in sample_iter]) == 100000


def test_sample__memory_overhead(ttn_sampler, output_fingerprinter):
    sample_iter = ttn_sampler.sample(['C=N']*1000, 100000,
                                     output_fingerprinter)
    samples = [sample for sample in sample_iter]
    size = sys.getsizeof(samples) / 1024 / 1024 / 1024.0
    print(f"Size: {size}GB")
    assert size < 1.0
