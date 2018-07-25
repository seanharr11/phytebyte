import pytest
import pickle
import numpy as np
from unittest.mock import Mock, MagicMock

from phytebyte import ROOT_DIR
from phytebyte.cache.encoded_smiles_cache import DictEncodedSmilesCache


test_root_dir = f'{ROOT_DIR}/../tests'
mock_cache = {'CN=O': np.zeros((1, 1024))}
with open(f'{test_root_dir}/.cache/daylight_numpy.pkl', 'wb') as f:
    pickle.dump(mock_cache, f)


def test_init():
    desc = DictEncodedSmilesCache(root_dir=test_root_dir)
    assert not desc.fp_type and not desc.encoding
    assert desc._root_dir == test_root_dir


@pytest.fixture
def desc():
    desc = DictEncodedSmilesCache(root_dir=test_root_dir)
    return desc


#def test_init():
#    desc = DictEncodedSmilesCache('daylight', 'numpy', root_dir=test_root_dir)
#    import os
#    print(os.listdir('/Users/kennywesterman/phytebyte/tests/.cache'))
#    assert all((desc._fp_type, desc._encoding, desc._filepath))
#    assert isinstance(desc._cache, dict)


def test_load(desc):
    desc.load('daylight', 'numpy')
    assert desc.fp_type == 'daylight' and desc.encoding == 'numpy'
    assert desc._cache
    with pytest.raises(Exception):
        desc.load('not_a_fp', 'not_an_encoding')


def test_get(desc):
    np_encoded_smiles = desc.get('CN=O', 'daylight', 'numpy')
    assert isinstance(np_encoded_smiles, np.ndarray)
    with pytest.raises(Exception):
        desc.get('Invalid-Key')


class myfp():
    @property
    def fp_type(self):
        return 'daylight'

    def fingerprint_and_encode(self, smiles, encoding, from_cache=True):
        return np.zeros((1, 1024))


def test_update(desc):
    desc.update('CN=NEW', myfp(), 'numpy')
    assert 'CN=NEW' in desc._cache.keys()
    with pytest.raises(Exception):
        desc.update('CN=NEW', myfp(), 'not_an_encoding')
    

def test_write(desc):
    desc.update('CN=NEW', myfp(), 'numpy')
    desc.write()
    with open(desc._filepath, 'rb') as f:
        temp = pickle.load(f)
    assert 'CN=NEW' in temp.keys()


def test_clear(desc):
    desc.clear()
    assert len(desc._cache.keys()) == 0
