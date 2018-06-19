import pytest
import sqlalchemy

from phytebyte.bioactive_cmpd.sources import ChemblRandomCompoundSmilesQuery


def test_init():
    q = ChemblRandomCompoundSmilesQuery(limit=100, excluded_smiles=['CC=N'])
    assert(q is not None)


def test_init__excluded_smiles_is_str():
    with pytest.raises(AssertionError):
        ChemblRandomCompoundSmilesQuery(limit=100, excluded_smiles='CC=N')


def test_init__limit_is_not_int():
    with pytest.raises(AssertionError):
        ChemblRandomCompoundSmilesQuery(limit="100", excluded_smiles=['CC=N'])


def test_build():
    q = ChemblRandomCompoundSmilesQuery(limit=100, excluded_smiles=['CC=N'])
    query = q.build()
    assert isinstance(query, sqlalchemy.sql.expression.Executable)
