import pybel
import pytest


@pytest.fixture
def mock_smiles():
    return "Cc1ccc(cc1O)C(C)C"


@pytest.fixture
def mock_molecule(mock_smiles):
    return pybel.readstring("smi", mock_smiles)


@pytest.fixture
def mock_bit_string():
    return "11110001"
