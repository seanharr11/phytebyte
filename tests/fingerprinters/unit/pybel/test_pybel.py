from phytebyte.fingerprinters.pybel import PybelFingerprinter

from bitarray import bitarray
import numpy as np
import pickle
import pytest
from unittest.mock import MagicMock, Mock


class PybelFingerprinterSubclass(PybelFingerprinter):
    @property
    def _pybel_fp_name(self):
        return "FP2"

    @property
    def _pybel_fp_length(self):
        return 1024


@pytest.fixture
def pybel_fp():
    class PybelFingerprinterSubclass(PybelFingerprinter):
        @property
        def _pybel_fp_name(self):
            return "FP2"

        @property
        def _pybel_fp_length(self):
            return 1024
    return PybelFingerprinterSubclass()


@pytest.fixture
def bad_pybel_fp():
    class PybelFingerprinterSubclass(PybelFingerprinter):
        @property
        def _pybel_fp_name(self):
            return "bad-bad-bad"

        @property
        def _pybel_fp_length(self):
            return 1024
    return PybelFingerprinterSubclass()


def test_smiles_to_nparray(pybel_fp, mock_smiles):
    mock_fp = Mock()
    mock_fp.bits = [True for _ in range(1024)]
    pybel_fp.smiles_to_fingerprint = MagicMock(return_value=mock_fp)
    nparray = pybel_fp.smiles_to_nparray(mock_smiles)
    assert len(nparray)
    assert nparray.dtype == 'uint8'
    assert np.array_equal(nparray, np.array(mock_fp.bits, dtype='uint8'))


def test_smiles_to_bitarray(pybel_fp, mock_smiles):
    mock_fp = Mock()
    mock_fp.bits = [i for i in range(1024) if i % 2 == 0]
    pybel_fp.smiles_to_fingerprint = MagicMock(return_value=mock_fp)
    bitarr = pybel_fp.smiles_to_bitarray(mock_smiles)
    assert bitarr == bitarray([i % 2 == 0 for i in range(1024)])


def test_smiles_to_fingerprint(pybel_fp, mock_smiles, mock_molecule):
    pybel_fp.smiles_to_molecule = MagicMock(return_value=mock_molecule)
    fp = pybel_fp.smiles_to_fingerprint(mock_smiles)
    assert fp
    assert hasattr(fp, 'bits')


def test_smiles_to_fingerprint__bad_fp_name(bad_pybel_fp, mock_molecule,
                                            mock_smiles):
    bad_pybel_fp.smiles_to_molecule = MagicMock(return_value=mock_molecule)
    with pytest.raises(ValueError):
        bad_pybel_fp.smiles_to_fingerprint(mock_smiles)


def test_fingerprinter_is_picklable():
    fp = PybelFingerprinterSubclass()
    pickle.dumps(fp)
