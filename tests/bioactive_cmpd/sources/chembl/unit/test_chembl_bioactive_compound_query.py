import pytest
import sqlalchemy
from phytebyte.bioactive_cmpd.sources.chembl.bioactivity import agonist_bioact_filter

from phytebyte.bioactive_cmpd.sources import (
    ChemblBioactiveCompoundQuery)


@pytest.fixture
def cbc_query():
    return ChemblBioactiveCompoundQuery(agonist_bioact_filter)


def test_init(cbc_query):
    cbc_q = ChemblBioactiveCompoundQuery(agonist_bioact_filter)
    assert(cbc_q)


def test_repr_is_implemented(cbc_query):
    assert "<ChemblBioactiveCompoundQuery" in repr(cbc_query)


def test_row_to_bioactive_compound(cbc_query):
    mock_row = (
        1000, 'pref_name', 'CC=NC', 'MOCK_GENE_TGT', 'name',
        [10, 20, 30],
        ['mg', 'ml', 'mg'],
        ['EC50', 'IC50', 'EC50'],
        ['Assay descr 1', 'Assay descr2', 'Assay descr3']
    )
    cbc_query.row_to_bioactive_compound(mock_row)


def test_build(cbc_query):
    q = cbc_query.build()
    assert isinstance(q, sqlalchemy.sql.expression.Executable)


def test_gene_tgts_is_str__raises_AssertionError():
    with pytest.raises(AssertionError):
        ChemblBioactiveCompoundQuery(agonist_bioact_filter, gene_tgts='HMGCR')


def test_compound_names_is_str__raises_AssertionError():
    with pytest.raises(AssertionError):
        ChemblBioactiveCompoundQuery(agonist_bioact_filter, compound_names='should be list')


def test_whereclause_default():
    cbc_q = ChemblBioactiveCompoundQuery(agonist_bioact_filter)
    query = cbc_q.build()
    assert "component_synonyms.component_synonym" not in str(
        query._whereclause)
    assert "compound_name" not in str(query._whereclause)


def test_whereclause_respects_gene_tgts():
    cbc_q = ChemblBioactiveCompoundQuery(
        agonist_bioact_filter,
        gene_tgts=['HMGCR'])
    query = cbc_q.build()
    assert "component_synonyms.component_synonym" in str(query._whereclause)


def test_whereclause_respects_compound_names():
    cbc_q = ChemblBioactiveCompoundQuery(
        agonist_bioact_filter,
        compound_names=['Dihydrogen Monoxide'])
    query = cbc_q.build()
    assert "compound_name" in str(query._whereclause)
