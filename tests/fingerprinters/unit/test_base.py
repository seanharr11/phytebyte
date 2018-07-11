from bitarray import bitarray
import numpy as np
import pytest

from phytebyte.fingerprinters.base import Fingerprinter


@pytest.fixture
def FingerprinterSubclass(mock_bit_string):
    class FingerprinterSubclass(Fingerprinter):
        def smiles_to_bitarray(self, smiles):
            return bitarray(mock_bit_string)

        def smiles_to_nparray(self, smiles):
            return np.array([bit for bit in mock_bit_string])
    return FingerprinterSubclass


@pytest.fixture
def subclassed_fingerprinter(FingerprinterSubclass):
    return FingerprinterSubclass()


def test_create_daylight():
    daylight_fp = Fingerprinter.create("daylight")
    assert daylight_fp


def test_create__bad_fp_name():
    with pytest.raises(Exception):
        Fingerprinter.create("foobar")


def test_smiles_to_bitarrays(subclassed_fingerprinter,
                             mock_bit_string, mock_smiles):
    bitarrays = subclassed_fingerprinter.smiles_to_bitarrays([mock_smiles])
    assert len(bitarrays) == 1
    assert bitarrays[0] == bitarray(mock_bit_string)


def test_smiles_to_bitarrays__bad_smiles_iter(subclassed_fingerprinter,
                                              mock_bit_string, mock_smiles):
    with pytest.raises(AssertionError):
        subclassed_fingerprinter.smiles_to_bitarrays(mock_smiles)


def test_smiles_to_nparrays(subclassed_fingerprinter,
                            mock_bit_string,
                            mock_smiles):
    np_arrays = subclassed_fingerprinter.smiles_to_nparrays([mock_smiles])
    assert len(np_arrays) == 1
    assert np.array_equal(
        np_arrays[0], np.array([bit for bit in mock_bit_string]))


def test_smiles_to_nparrays__bad_smiles_iter(subclassed_fingerprinter,
                                             mock_bit_string, mock_smiles):
    with pytest.raises(AssertionError):
        subclassed_fingerprinter.smiles_to_nparrays(mock_smiles)


def test_bitarrays_to_nparrays(subclassed_fingerprinter, mock_bit_string):
    bitarrays = [bitarray(mock_bit_string), bitarray("11111000")]
    nparrays = subclassed_fingerprinter.bitarrays_to_nparrays(bitarrays)
    assert len(nparrays) == 2
    assert np.array_equal(
        nparrays[0],
        np.array([int(bit) for bit in mock_bit_string], dtype='bool'))


def test_fingerprint_and_encode__numpy(subclassed_fingerprinter, mock_smiles):
    nd_arr = subclassed_fingerprinter.fingerprint_and_encode(mock_smiles,
                                                             'numpy')
    assert isinstance(nd_arr, np.ndarray)


def test_fingerprint_and_encode__bitarray(subclassed_fingerprinter,
                                          mock_smiles):
    bitarr = subclassed_fingerprinter.fingerprint_and_encode(mock_smiles,
                                                             'bitarray')
    assert isinstance(bitarr, bitarray)
