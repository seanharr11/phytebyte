from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from typing import List

from phytebyte.food_cmpd.types import FoodCmpd, FoodContent

class FoodCmpdSource(ABC):
    def __init__(self, db_url):
        engine = create_engine(db_url)
        self.conn = engine.connect()

    @abstractmethod
    def fetch_all_cmpds(self) -> List[FoodCmpd]:
        """
        Fetch a `FoodCmpd` for each unique ID in the database.
        """
        pass


    @abstractmethod
    def fetch_foods(self, food_cmpd_ids: List[int]) -> List[FoodContent]:
        """
        Fetch any foods containing any of the provided food compound ids as
        `FoodContent` objects.

        `food_cmpd_ids`: List of integers corresponding to food compounds IDs
        for the database in question.
        """
        pass
