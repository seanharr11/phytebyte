from typing import List, Iterator

from phytebyte.food_cmpd.sources import FoodCmpdSource
from phytebyte.food_cmpd import FoodCmpd, FoodContent
from .queries import (
    FoodbFoodCmpdQuery, FoodbFoodCmpdSmilesOnlyQuery, FoodbFoodsFromCmpdQuery)


class FoodbFoodCmpdSource(FoodCmpdSource):
    def fetch_all_cmpds(self) -> Iterator[FoodCmpd]:
        query = FoodbFoodCmpdQuery()
        executable_query = query.build()
        conn = self.engine.connect()
        conn.execution_options(stream_results=True)
        iterator = conn.execute(executable_query)
        cnt = 0
        while True:
            chunk = iterator.fetchmany(1000)
            cnt += 1
            if not chunk:
                break
            for row in chunk:
                yield query.row_to_food_cmpd(row, self)

    def fetch_all_cmpd_smiles(self) -> Iterator[str]:
        query = FoodbFoodCmpdSmilesOnlyQuery()
        executable_query = query.build()
        conn = self.engine.connect()
        conn.execution_options(stream_results=True)
        iterator = conn.execute(executable_query)
        cnt = 0
        while True:
            chunk = iterator.fetchmany(1000)
            cnt += 1
            if not chunk:
                break
            for row in chunk:
                yield row[0]

    def fetch_foods(self, food_cmpd_uid: int) -> List[FoodContent]:
        query = FoodbFoodsFromCmpdQuery(food_cmpd_uid)
        executable_query = query.build()
        return [query.row_to_food_content(row)
                for row in self.engine.connect().execute(executable_query)]
