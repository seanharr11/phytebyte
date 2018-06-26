import pytest
import sqlalchemy

from phytebyte.food_cmpd.sources import FoodbFoodCmpdQuery


@pytest.fixture
def ffc_query():
    return FoodbFoodCmpdQuery()


def test_init(ffc_query):
    assert ffc_query


def test_repr_is_implemented(ffc_query):
    assert "<FoodbFoodCmpdQuery" in repr(ffc_query)


def test_row_to_food_cmpd(ffc_query):
    mock_row = (123, 'CCcNd12(4cc)', 'Resveratrol', 'This is a compound.')
    ffc_query.row_to_food_cmpd(mock_row, 'my_source')


def test_build(ffc_query):
    q = ffc_query.build()
    assert isinstance(q, sqlalchemy.sql.expression.Executable)
