import pytest

from phytebyte.fingerprinters.pybel import (
    PybelDeserializer, SmilesDeserializationError)


def test_smiles_to_molecule(mock_smiles):
    pd = PybelDeserializer()
    mol = pd.smiles_to_molecule(mock_smiles)
    assert mol


def test_smiles_to_molecule__bad_smile__handle_exc():
    pd = PybelDeserializer()
    with pytest.raises(SmilesDeserializationError):
        pd.smiles_to_molecule("C=BAD")
