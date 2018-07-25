import pytest
import sqlalchemy

from phytebyte.food_cmpd.sources import FoodbFoodsFromCmpdQuery


@pytest.fixture
def fffc_query():
    return FoodbFoodsFromCmpdQuery(123)


def test_init(fffc_query):
    assert fffc_query


def test_repr_is_implemented(fffc_query):
    assert "<FoodbFoodsFromCmpdQuery" in repr(fffc_query)


def test_row_to_food(fffc_query):
    mock_row = ('food1', 'a food', 'rind', 5, 'ppm', 1, 10, 5)
    fffc_query.row_to_food_content(mock_row)


def test_build(fffc_query):
    q = fffc_query.build()
    assert isinstance(q, sqlalchemy.sql.expression.Executable)


def test_food_cmpd_uid_is_int__raises_AssertionError():
    with pytest.raises(AssertionError):
        FoodbFoodsFromCmpdQuery(food_cmpd_uid='strID')


def test_whereclause(fffc_query):
    q = fffc_query.build()
    assert "contents.source_type" in str(q._whereclause)
    assert "compounds.id =" in str(q._whereclause)


def test_order_by(fffc_query):
    ob_str = ', '.join([str(ob) for ob in fffc_query._order_by])
    print(str(fffc_query._order_by[0]))
    assert "contents.orig_content DESC" in ob_str
    assert "contents.standard_content DESC" in ob_str
    assert "contents.orig_max DESC" in ob_str
    assert "contents.orig_min DESC" in ob_str
