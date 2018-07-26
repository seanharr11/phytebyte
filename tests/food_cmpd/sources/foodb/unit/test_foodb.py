import math
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


class MockRowProxy():
    fetchmany_calls = 0

    def __init__(self, num_fetchmany_calls, num_rows):
        self.num_fetchmany_calls = num_fetchmany_calls
        self.num_rows = num_rows

    def fetchmany(self, _):
        if self.fetchmany_calls == self.num_fetchmany_calls:
            return None
        self.fetchmany_calls += 1
        rows_per_call = math.ceil(self.num_rows / self.num_fetchmany_calls)
        return [[1] for _ in range(rows_per_call)]


def test_fetch_all_cmpds(ffc_source, monkeypatch):
    mock_result_proxy = MockRowProxy(num_fetchmany_calls=2,
                                     num_rows=4)
    mock_conn = Mock()
    mock_conn.execute = MagicMock(return_value=mock_result_proxy)
    mock_engine = Mock()
    mock_engine.connect = MagicMock(return_value=mock_conn)
    monkeypatch.setattr(
        "phytebyte.food_cmpd.sources.base.create_engine",
        MagicMock(return_value=mock_engine))
    assert len([foo for foo in ffc_source.fetch_all_cmpds()]) == 4


def test_fetch_foods(ffc_source, monkeypatch):
    mock_rows = [1] * 4
    mock_conn = Mock()
    mock_conn.execute = MagicMock(return_value=mock_rows)
    mock_engine = Mock()
    mock_engine.connect = MagicMock(return_value=mock_conn)
    monkeypatch.setattr(
        "phytebyte.food_cmpd.sources.base.create_engine",
        MagicMock(return_value=mock_engine))

    assert len(ffc_source.fetch_foods(100)) == 4
