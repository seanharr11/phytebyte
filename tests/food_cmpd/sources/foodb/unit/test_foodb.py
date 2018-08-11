from unittest.mock import Mock, MagicMock
import pytest

from phytebyte.food_cmpd.sources import FoodbFoodCmpdSource


@pytest.fixture
def mock_rows():
    return [
        ["row_1_val_1", "row_1_val_2"],
        ["row_2_val_1", "row_2_val_2"]]


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
def ffc_source(mock_ffc_query_class,
               mock_fffc_query_class,
               monkeypatch):
    monkeypatch.setattr("phytebyte.food_cmpd.sources.foodb.foodb."
                        "FoodbFoodCmpdQuery",
                        mock_ffc_query_class)
    monkeypatch.setattr("phytebyte.food_cmpd.sources.foodb.foodb."
                        "FoodbFoodsFromCmpdQuery",
                        mock_fffc_query_class)
    source = FoodbFoodCmpdSource("db_url://compound-interest")
    return source


def test_fetch_all_cmpds(ffc_source, monkeypatch, mock_rows,
                         mock_streaming_engine_factory):
    mock_engine = mock_streaming_engine_factory(mock_rows, 2)
    monkeypatch.setattr(
        "phytebyte.food_cmpd.sources.base.create_engine",
        MagicMock(return_value=mock_engine))
    assert len([foo for foo in ffc_source.fetch_all_cmpds()]) == 2


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
