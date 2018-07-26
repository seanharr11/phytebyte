from functools import partial
from typing import List, Iterator, Callable

from phytebyte.food_cmpd.sources import FoodCmpdSource
from phytebyte.food_cmpd import FoodCmpd, FoodContent
from .queries import FoodbFoodCmpdQuery, FoodbFoodsFromCmpdQuery


class FoodbFoodCmpdSource(FoodCmpdSource):
    def fetch_all_cmpds(self) -> Iterator[Callable[[], FoodCmpd]]:
        query = FoodbFoodCmpdQuery()
        executable_query = query.build()
        conn = self.engine.connect()
        conn.execution_options(stream_results=True)
        iterator = conn.execute(executable_query)
        while True:
            chunk = iterator.fetchmany(1000)
            if not chunk:
                break
            for row in chunk:
                yield partial(query.row_to_food_cmpd, row, self)

    def fetch_foods(self, food_cmpd_uid: int) -> List[FoodContent]:
        query = FoodbFoodsFromCmpdQuery(food_cmpd_uid)
        executable_query = query.build()
        return [query.row_to_food_content(row)
                for row in self.engine.connect().execute(executable_query)]
