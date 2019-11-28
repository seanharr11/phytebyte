from unittest.mock import Mock, MagicMock
import pytest


from phytebyte.bioactive_cmpd.sources import ChemblBioactiveCompoundSource


@pytest.fixture
def mock_rows():
    return ["mock1", "mock2", "mock3", "mock4"]


@pytest.fixture
def mock_bioactive_compound():
    return Mock()


@pytest.fixture
def mock_cbc_query_class(mock_bioactive_compound):
    mock_cbc_query = Mock()
    mock_cbc_query.build = MagicMock(
        return_value=Mock())
    mock_cbc_query.row_to_bioactive_compound = MagicMock(
        return_value=mock_bioactive_compound)
    return MagicMock(return_value=mock_cbc_query)


@pytest.fixture
def mock_crcs_query_class():
    mock_cbc_query = Mock()
    mock_cbc_query.build = MagicMock(return_value=Mock())
    return MagicMock(return_value=mock_cbc_query)


@pytest.fixture
def cbc_source(mock_streaming_engine_factory,
               mock_rows,
               mock_cbc_query_class,
               mock_crcs_query_class,
               monkeypatch):
    mock_create_engine_func = MagicMock(
        return_value=mock_streaming_engine_factory(mock_rows, 2))
    monkeypatch.setattr("phytebyte.bioactive_cmpd.sources.base.create_engine",
                        mock_create_engine_func)
    monkeypatch.setattr(
        "phytebyte.bioactive_cmpd.sources.chembl.chembl."
        "ChemblBioactiveCompoundQuery",
        mock_cbc_query_class)
    monkeypatch.setattr(
        "phytebyte.bioactive_cmpd.sources.chembl.chembl."
        "ChemblRandomCompoundSmilesQuery",
        mock_crcs_query_class)
    monkeypatch.setattr(
        "phytebyte.bioactive_cmpd.sources.chembl.chembl."
        "ChemblBioactiveCompoundQuery",
        mock_cbc_query_class)
    source = ChemblBioactiveCompoundSource("db_url://doesnt-matter", .5)
    return source


def test_fetch_with_gene_tgts(cbc_source, mock_bioactive_compound):
    partial_iter = cbc_source.fetch_with_gene_tgts(['HMGCR'], 'agonist')
    assert hasattr(partial_iter, '__next__')
    first_partial = next(partial_iter)
    assert callable(first_partial)
    assert first_partial() == mock_bioactive_compound


def test_fetch_with_compound_names(cbc_source, mock_bioactive_compound):
    partial_iter = cbc_source.fetch_with_compound_names(
        ['compound1', 'compound2'])
    assert hasattr(partial_iter, '__next__')
    first_partial = next(partial_iter)
    assert callable(first_partial)
    assert first_partial() == mock_bioactive_compound


def test_random_compounds_exc_smiles(monkeypatch, cbc_source,
                                     mock_streaming_engine_factory):
    mock_rows = [['CC=N'], ['CC=O']]
    mock_engine = mock_streaming_engine_factory(mock_rows, 1)

    monkeypatch.setattr("phytebyte.bioactive_cmpd.sources.base.create_engine",
                        MagicMock(return_value=mock_engine))

    smiles_iter = cbc_source.fetch_random_compounds_exc_smiles(100, ['CC=P'])
    assert hasattr(smiles_iter, '__next__')
    first_smile = next(smiles_iter)
    assert first_smile == "CC=N"
    second_smile = next(smiles_iter)
    assert second_smile == "CC=O"
