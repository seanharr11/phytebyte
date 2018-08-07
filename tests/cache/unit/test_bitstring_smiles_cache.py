import pytest
import json
import numpy as np

from phytebyte import ROOT_DIR
from phytebyte.cache.bitstring_smiles_cache import JsonBitstringSmilesCache


@pytest.fixture
def fp_type():
    return 'daylight'


@pytest.fixture
def cache_root_dir(fp_type):
    root_dir = f'{ROOT_DIR}/../tests'
    mock_cache = {'CN=O': '01' * 512}
    cache_filename = f'{root_dir}/.cache/{fp_type}.json'
    with open(cache_filename, 'w') as f:
        json.dump(mock_cache, f)
    return root_dir


@pytest.fixture
def myfp(fp_type):
    class MockFingerprinter():
        @property
        def fp_type(self):
            return fp_type

        def fingerprint_and_encode(self, smiles, encoding, from_cache=True):
            return np.zeros((1, 1024))

        def smiles_to_bitstring(self, smiles):
            return "01" * 512

    return MockFingerprinter()


@pytest.fixture
def empty_cache(cache_root_dir, fp_type):
    cache = JsonBitstringSmilesCache(fp_type, root_dir=cache_root_dir)
    return cache


@pytest.fixture
def loaded_cache(cache_root_dir, fp_type):
    cache = JsonBitstringSmilesCache(fp_type, root_dir=cache_root_dir)
    cache.load()
    return cache


def test_init(cache_root_dir, fp_type):
    cache = JsonBitstringSmilesCache(fp_type, root_dir=cache_root_dir)
    assert cache._root_dir == cache_root_dir
    assert cache._cache is None
    assert cache._fp_type == fp_type


def test_load(empty_cache):
    empty_cache.load()
    assert list(empty_cache._cache.keys()) == ['CN=O']


def test_get(loaded_cache):
    np_encoded_smiles = loaded_cache.get('CN=O')
    assert np_encoded_smiles is not None
    assert isinstance(np_encoded_smiles, str)


def test_update(loaded_cache, myfp):
    loaded_cache.update('CN=NEW', myfp)
    assert 'CN=NEW' in loaded_cache._cache.keys()


def test_write(loaded_cache, myfp):
    loaded_cache.update('CN=NEW', myfp)
    loaded_cache.write()
    loaded_cache.clear()
    loaded_cache.load()
    assert 'CN=NEW' in loaded_cache._cache.keys()


def test_clear(loaded_cache):
    loaded_cache.clear()
    assert len(loaded_cache._cache.keys()) == 0
