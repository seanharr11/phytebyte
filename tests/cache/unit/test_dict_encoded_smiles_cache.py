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
    desc = DictEncodedSmilesCache('daylight', 'numpy', root_dir=test_root_dir)
    import os
    print(os.listdir('/Users/kennywesterman/phytebyte/tests/.cache'))
    assert all((desc._fp_type, desc._encoding, desc._filepath))
    assert isinstance(desc._cache, dict)


@pytest.fixture
def desc():
    desc = DictEncodedSmilesCache('daylight', 'numpy', root_dir=test_root_dir)
    return desc


def test_get(desc):
    np_encoded_smiles = desc.get('CN=O')
    assert isinstance(np_encoded_smiles, np.ndarray)
    with pytest.raises(Exception):
        desc.get('Invalid-Key')


@pytest.fixture
def myfp():
    myfp = Mock()
    myfp.fingerprint_and_encode = MagicMock(return_value=np.zeros((1,1024)))
    return myfp


def test_update(desc, myfp):
    desc.update('CN=NEW', myfp)
    assert 'CN=NEW' in desc._cache.keys()
    

def test_write(desc, myfp):
    desc.update('CN=NEW', myfp)
    desc.write()
    with open(desc._filepath, 'rb') as f:
        temp = pickle.load(f)
    assert 'CN=NEW' in temp.keys()


def test_clear(desc):
    desc.clear()
    assert len(desc._cache.keys()) == 0
