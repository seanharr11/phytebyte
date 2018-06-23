from typing import List

from phytebyte.food_cmpd.sources import FoodCmpdSource
from phytebyte.food_cmpd import FoodCmpd, FoodContent
from .queries import FoodbFoodCmpdQuery, FoodbFoodsFromCmpdQuery


class FoodbFoodCmpdSource(FoodCmpdSource):
    def fetch_all_cmpds(self) -> List[FoodCmpd]:
        query = FoodbFoodCmpdQuery()
        executable_query = query.build()
        return [query.row_to_food_cmpd(row, self)
                for row in self.conn.execute(executable_query)]

    def fetch_foods(self, food_cmpd_uid: int) -> List[FoodContent]:
        query = FoodbFoodsFromCmpdQuery(food_cmpd_uid)
        executable_query = query.build()
        return [query.row_to_food_content(row)
                for row in self.conn.execute(executable_query)]
