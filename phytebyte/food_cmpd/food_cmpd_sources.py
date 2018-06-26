from sqlalchemy import create_engine
from sqlalchemy import text
from collections import namedtuple
from typing import List


class FoodCmpd:
    def __init__(self, source, id_, smiles, name, descr, conn):
        self.source = source
        self.id = id_
        self.smiles = smiles
        self.name = name
        self.descr = descr
        self.conn = conn

    @property
    def foods(self) -> List[Food]:
        q = text("""
            SELECT foods.name, foods.description, contents.orig_food_part,
                   contents.orig_content, contents.orig_unit,
                   contents.orig_min, contents.orig_max,
                   contents.standard_content
            FROM foods
            INNER JOIN contents
             ON contents.food_id = foods.id
            INNER JOIN compounds
             ON compounds.id = contents.source_id
            WHERE contents.source_type = 'Compound'
             AND compounds.id = :compound_id
            ORDER BY contents.orig_content, contents.standard_content,
                     contents.orig_max, contents.orig_min DESC
            LIMIT 25""")
        return [Food(*r) for r in
                self.conn.execute(q, compound_id=self.id).fetchall()]

    @staticmethod
    def get_amount(food: Food):
        amt = food.content or food.amount or food.max or food.min
        amt = round(amt, 2) if amt else None
        return amt

    @staticmethod
    def get_units(food: Food):
        return f"{food.unit}"

    def print_foods(self,
               ignore_if_no_food=False,
               ignore_if_no_food_content=False):
        food_bullets = "\n".join(
            [f" - {food.food_name} ({food.food_part}) "
             f"{self.get_amount(food)} {self.get_units(food)}"
             for food in self.foods
             if not (ignore_if_no_food_content and not self.get_amount(food))])
        return "" if not food_bullets and ignore_if_no_food else\
            f"*Food Compound: {self.name}\n"\
            f"{food_bullets}\n"


class FooDbConnection():
    def __init__(self, db_url):
        self._engine = create_engine(db_url)
        self.conn = self._engine.connect()

    def fetch_compounds(self):
        q = """SELECT c.id, c.moldb_smiles AS smiles, c.name, c.description FROM compounds c"""
        return [FoodCmpd('FooDB', *r, self.conn) for r in self.conn.execute(q).fetchall()]
            
