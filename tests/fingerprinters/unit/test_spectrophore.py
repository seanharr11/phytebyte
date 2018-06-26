import pytest
from unittest.mock import MagicMock


from phytebyte.fingerprinters.pybel import SpectrophoreFingerprinter


def test_init():
    sfp = SpectrophoreFingerprinter()
    assert sfp


def test_smiles_to_nparray(mock_molecule, mock_smiles):
    sfp = SpectrophoreFingerprinter()
    sfp.smiles_to_molecule = MagicMock(return_value=mock_molecule)
    spect_nparray = sfp.smiles_to_nparray(mock_smiles)
    assert len(spect_nparray)
    assert spect_nparray.dtype == "float64"


def test_smiles_to_bitarray__NotImplemented(mock_smiles):
    sfp = SpectrophoreFingerprinter()
    with pytest.raises(NotImplementedError):
        sfp.smiles_to_bitarray(mock_smiles)
