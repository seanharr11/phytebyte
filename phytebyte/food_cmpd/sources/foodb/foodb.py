from typing import List

from phytebyte.food_cmpd.sources import FoodCmpdSource
from phytebyte.food_cmpd import FoodCmpd, FoodContent
from .queries import FoodbFoodCmpdQuery


class FoodbFoodCmpdSource(FoodCmpdSource):
    def fetch_all_cmpds(self) -> List[FoodCmpd]:
        query = FoodbFoodCmpdQuery()
        executable_query = query.build()
        return [row for row in self.conn.execute(executable_query)]

    def fetch_foods(self, food_cmpd_uids: List[int]) -> List[FoodContent]:
        query = FoodbFoodsFromCmpdQuery(food_cmpd_uid)
        executable_query = query.build()
        return [row for row in self.conn.execute(executable_query)]
