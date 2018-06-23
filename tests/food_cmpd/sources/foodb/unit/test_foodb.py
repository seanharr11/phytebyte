from unittest.mock import Mock, MagicMock
import pytest

from phytebyte.food_cmpd.sources import FoodbFoodCmpdSource


@pytest.fixture
def mock_row_iter():
    return [
        ["mock1", "mock2"],
        ["mock3", "mock4"]]


@pytest.fixture
def mock_connection(mock_row_iter):
    conn = Mock()
    conn.execute = MagicMock(return_value=mock_row_iter)
    return conn


@pytest.fixture
def mock_engine(mock_connection):
    e = Mock()
    e.connect = MagicMock(return_value=mock_connection)
    return e


@pytest.fixture
def mock_create_engine_func(mock_engine):
    m = MagicMock(return_value=mock_engine)
    return m


@pytest.fixture
def mock_food_cmpd():
    return Mock()


@pytest.fixture
def mock_food_content():
    return Mock()


@pytest.fixture
def mock_ffc_query_class(mock_food_cmpd):
    mock_ffc_query = Mock()
    mock_ffc_query.build = MagicMock(return_value=Mock())
    mock_ffc_query.row_to_food_cmpd = MagicMock(
        return_value=mock_food_cmpd)
    return MagicMock(return_value=mock_ffc_query)


@pytest.fixture
def mock_fffc_query_class():
    mock_fffc_query = Mock()
    mock_fffc_query.build = MagicMock(return_value=Mock())
    return MagicMock(return_value=mock_fffc_query)


@pytest.fixture
def ffc_source(mock_create_engine_func,
                mock_ffc_query_class,
                mock_fffc_query_class,
                monkeypatch):
    monkeypatch.setattr("phytebyte.food_cmpd.sources.base.create_engine",
                        mock_create_engine_func)
    monkeypatch.setattr("phytebyte.food_cmpd.sources.foodb.foodb."
                        "FoodbFoodCmpdQuery",
                        mock_ffc_query_class)
    monkeypatch.setattr("phytebyte.food_cmpd.sources.foodb.foodb."
                        "FoodbFoodsFromCmpdQuery",
                        mock_fffc_query_class)
    source = FoodbFoodCmpdSource("db_url://compound-interest") 
    return source


def test_fetch_all_cmpds(ffc_source):

    mock_rows = [1] * 4
    ffc_source.conn.execute = MagicMock(return_value=mock_rows)
    assert len(ffc_source.fetch_all_cmpds()) == 4


def test_fetch_foods(ffc_source):
    mock_rows = [1] * 4
    ffc_source.conn.execute = MagicMock(return_value=mock_rows)
    assert len(ffc_source.fetch_foods(100)) == 4
