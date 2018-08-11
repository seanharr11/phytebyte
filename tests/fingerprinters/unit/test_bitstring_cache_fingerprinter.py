from bitarray import bitarray
import numpy as np
import pytest
from unittest.mock import Mock, MagicMock

from phytebyte.fingerprinters.bitstring_cache_fingerprinter import (
    BitstringCacheFingerprinter)


@pytest.fixture
def mock_cache():
    cache = Mock()
    return cache


@pytest.fixture
def mock_ndarray():
    return Mock()


@pytest.fixture
def mock_bitarray():
    return Mock()


@pytest.fixture
def BitstringCacheFingerprinterSub(mock_bitarray, mock_ndarray):
    class BSCFPSubclass(BitstringCacheFingerprinter):
        def fp_type():
            return Mock()

        def smiles_to_bitarray(self, smiles):
            return mock_bitarray

        def smiles_to_nparray(self, smiles):
            return mock_ndarray
    return BSCFPSubclass


@pytest.fixture
def bitstring_cache_fp(BitstringCacheFingerprinterSub):
    return BitstringCacheFingerprinterSub()


@pytest.fixture
def bitstring_cache_fp_w_cache(BitstringCacheFingerprinterSub, mock_cache):
    class BitstringCacheFingerprinterSubSub(BitstringCacheFingerprinterSub):
        pass
    BitstringCacheFingerprinterSubSub.set_cache(mock_cache)
    return BitstringCacheFingerprinterSubSub()


def test_fp_subclasses_do_not_share_cache_class_attr(
        bitstring_cache_fp_w_cache,
        mock_cache,
        bitstring_cache_fp):
    assert bitstring_cache_fp._bitstring_cache is None
    assert bitstring_cache_fp_w_cache._bitstring_cache == mock_cache


def test_smiles_to_bitstring__calls_smiles_to_nparray(
        mock_ndarray,
        BitstringCacheFingerprinterSub):
    bcf = BitstringCacheFingerprinterSub()
    bcf.smiles_to_nparray = MagicMock()
    bcf.nparray_to_bitstring = MagicMock()
    bcf.smiles_to_bitstring(Mock())
    bcf.smiles_to_nparray.assert_called_once()


def test_smiles_to_bitstring__calls_nparray_to_bitstring(
        mock_ndarray,
        BitstringCacheFingerprinterSub):
    bcf = BitstringCacheFingerprinterSub()
    bcf.smiles_to_nparray = MagicMock()
    bcf.nparray_to_bitstring = MagicMock()
    bcf.smiles_to_bitstring(Mock())
    bcf.nparray_to_bitstring.assert_called_once()


def test_nparray_to_bitstring(BitstringCacheFingerprinterSub):
    bcf = BitstringCacheFingerprinterSub()
    bitstring = bcf.nparray_to_bitstring(np.zeros(500, np.uint8))
    assert bitstring == ("0" * 500)


def test_bitarray_to_bitstring(BitstringCacheFingerprinterSub):
    bcf = BitstringCacheFingerprinterSub()
    bitstring = "101010101010101"
    assert bitstring == bcf.bitarray_to_bitstring(bitarray(bitstring))


def test_bitstring_to_nparray(BitstringCacheFingerprinterSub):
    bcf = BitstringCacheFingerprinterSub()
    bitstring = "1010"
    assert np.array_equal(np.array([1, 0, 1, 0], np.uint8),
                          bcf.bitstring_to_nparray(bitstring))


def test_bitstring_to_bitarray(BitstringCacheFingerprinterSub):
    bcf = BitstringCacheFingerprinterSub()
    bitstring = "1010"
    assert bitarray(bitstring) == bcf.bitstring_to_bitarray(bitstring)
