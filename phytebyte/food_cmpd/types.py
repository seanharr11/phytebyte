from collections import namedtuple
from typing import List


FoodContent = namedtuple(
    "FoodContent", ["food_name", "food_descr", "food_part", "content", "unit",
                    "min", 'max', 'amount'])


class FoodCmpd:
    def __init__(self, source, uid_, smiles, name, descr):
        self.source = source
        self.uid = uid_
        self.smiles = smiles
        self.name = name
        self.descr = descr

    @property
    def foods(self) -> List[FoodContent]:
        return [f for f in self.source.fetch_foods(self.uid)]

    @staticmethod
    def get_amount(food: FoodContent):
        amt = food.content or food.amount or food.max or food.min
        amt = round(amt, 2) if amt else None
        return amt

    @staticmethod
    def get_units(food: FoodContent):
        return f"{food.unit}"

    def get_food_info_str(self,
                          ignore_if_no_food=False,
                          ignore_if_no_food_content=False):
        food_bullets = "\n".join(
            [f" - {food.food_name} ({food.food_part}) "
             f"{self.get_amount(food)} {self.get_units(food)}"
             for food in self.foods
             if not (ignore_if_no_food_content and not self.get_amount(food))])
        return None if not food_bullets and ignore_if_no_food else\
            f"* Food Compound: {self.name}\n"\
            f"{food_bullets}\n"
