from functools import partial
from pathos.pools import ProcessPool as Pool
import os

from phytebyte.food_cmpd.sources import FoodbFoodCmpdSource
from phytebyte.bioactive_cmpd.sources import (
    ChemblBioactiveCompoundSource)
from phytebyte.fingerprinters import Fingerprinter
from phytebyte.cache import RedisEncodedSmilesCache

myfp = Fingerprinter.create('daylight')
myfcs = FoodbFoodCmpdSource(os.environ['FOODB_URL'])
mybcs = ChemblBioactiveCompoundSource(os.environ['CHEMBL_DB_URL'])

mycache = RedisEncodedSmilesCache()

target_gene_chembl_cmpds = list(mybcs.fetch_with_gene_tgts(['HMGCR']))
"""
all_food_cmpds = myfcs.fetch_all_cmpds()

# Food Compounds
for c in all_food_cmpds:
    mycache.update(c().smiles, myfp, "numpy")
# Copmounds targeting gene
for c in target_gene_chembl_cmpds:
    mycache.update(c().smiles, myfp, "numpy")
    mycache.update(c().smiles, myfp, "bitarray")
# Negative Sampler
mycache.disconnect()
cnt = 0
"""
print("Negative Sample Cache...")
mycache.connect("daylight", "numpy")
assert mycache._redis is not None
all_smiles_iter = mybcs.fetch_random_compounds_exc_smiles(
    excluded_smiles=[part().smiles for part in target_gene_chembl_cmpds],
    limit=1700000)
mycache.disconnect()
print("Obtained smiles_iter")
print("Fingerprinting numpy...")


class Processor():
    def __init__(self, cache, fingerprinter, encoding):
        self.cache = cache
        self.fingerprinter = fingerprinter
        self.encoding = encoding

    def __call__(self, smiles):
        self.cache.update(smiles, self.fingerprinter, self.encoding)


with Pool(processes=8) as pool:
    [_ for _ in pool.uimap(
        Processor(mycache, fingerprinter=myfp, encoding="numpy"),
        all_smiles_iter)]
print("Done.")
print("Fingerprinting bitarray.")
with Pool(processes=8) as pool:
    [_ for _ in pool.uimap(partial(mycache.update, fingerprinter=myfp,
                           encoding="bitarray"),
     all_smiles_iter)]
print("Done.")
print("Saving to disk...")
mycache.connect('fp_type', 'encoding')
mycache.write()
print("Done.")
