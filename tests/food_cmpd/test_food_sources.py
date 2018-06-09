from phytebyte import food_cmpd as fc
import os


def test_foodb():
    my_conn = fc.FooDbConnection(os.environ['FOODB_URL'])
    my_cmpds = my_conn.fetch_compounds()
    for c in my_cmpds[:5]:
        print(c.print_foods())
