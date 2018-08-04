from sqlalchemy import select, and_, desc
from phytebyte import Query
from phytebyte.food_cmpd.types import FoodCmpd, FoodContent
from .models import Compound, Content, Food


class FoodbFoodCmpdQuery(Query):
    def __init__(self):
        pass

    def __repr__(self):
        return self.__class__.__name__

    @staticmethod
    def row_to_food_cmpd(row, source) -> FoodCmpd:
        return FoodCmpd(source, *row)

    @property
    def _select(self):
        return select([
            Compound.id.label("uid"),
            Compound.moldb_smiles.label("smiles"),
            Compound.name,
            Compound.description])

    @property
    def _select_from(self):
        return Compound.__table__

    @property
    def _order_by(self):
        return (Compound.id,)


class FoodbFoodCmpdSmilesOnlyQuery(FoodbFoodCmpdQuery):
    @property
    def _select(self):
        return select([
            Compound.moldb_smiles.label("smiles")])


class FoodbFoodsFromCmpdQuery(Query):
    def __init__(self,
                 food_cmpd_uid: int):
        self._food_cmpd_uid = food_cmpd_uid
        assert self._food_cmpd_uid is None or isinstance(
            self._food_cmpd_uid, int)

    def __repr__(self):
        return f"""<FoodbFoodsFromCmpdQuery
            {self._food_cmpd_uid}>"""

    @staticmethod
    def row_to_food_content(row) -> FoodContent:
        return FoodContent(*row)

    @property
    def _select(self):
        return select([
            Food.name,
            Food.description,
            Content.orig_food_part,
            Content.orig_content,
            Content.orig_unit,
            Content.orig_min,
            Content.orig_max,
            Content.standard_content])

    @property
    def _select_from(self):
        return(
            Food.__table__
            .join(Content,
                  Food.id == Content.food_id)
            .join(Compound,
                  Content.source_id == Compound.id))

    @property
    def _whereclause(self):
        return and_(
            Content.source_type == "Compound",
            Compound.id == self._food_cmpd_uid)

    @property
    def _order_by(self):
        order_by_tuple = (
            desc(Content.orig_content),
            desc(Content.standard_content),
            desc(Content.orig_max),
            desc(Content.orig_min))
        return order_by_tuple
