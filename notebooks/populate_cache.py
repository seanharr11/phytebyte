import os

from phytebyte.food_cmpd.sources import FoodbFoodCmpdSource
from phytebyte.bioactive_cmpd.sources import (
    ChemblBioactiveCompoundSource)
from phytebyte.fingerprinters import Fingerprinter
from phytebyte.cache import BitstringSmilesCache

myfp = Fingerprinter.create('daylight')
myfcs = FoodbFoodCmpdSource(os.environ['FOODB_URL'])
mybcs = ChemblBioactiveCompoundSource(os.environ['CHEMBL_DB_URL'])

bitstring_cache = BitstringSmilesCache.create("json")

bitstring_cache.load()
target_gene_chembl_cmpds = mybcs.fetch_with_gene_tgts(['HMGCR'])

all_food_cmpds = myfcs.fetch_all_cmpds()

# Food Compounds
cnt = 0
for c in all_food_cmpds:
    cnt += 1
    if cnt % 1000 == 0:
        print(f"Fingerprinted '{cnt}' Food Compounds")
    bitstring_cache.update(c.smiles, myfp)
# Copmounds targeting gene
cnt = 0
for c in target_gene_chembl_cmpds:
    cnt += 1
    if cnt % 100 == 0:
        print(f"Fingerprinted '{cnt}' Target Gene Compounds")
    bitstring_cache.update(c().smiles, myfp)
    bitstring_cache.update(c().smiles, myfp)
# Negative Sampler
cnt = 0
print("Negative Sample Cache...")
all_smiles_iter = mybcs.fetch_random_compounds_exc_smiles(
    excluded_smiles=[part().smiles for part in target_gene_chembl_cmpds],
    limit=1700000)
print("Obtained smiles_iter")
print("Fingerprinting negative samples...")
cnt = 0
for smiles in all_smiles_iter:
    cnt += 1
    if cnt % 1000 == 0:
        print(f"Fingerprinted '{cnt}' Negative Samples")
    bitstring_cache.update(smiles, myfp)
    bitstring_cache.update(smiles, myfp)
print("Writing to disk.")
bitstring_cache.write()
print("Done.")
