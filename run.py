# coding: utf-8
from phytebyte import PhyteByte
from phytebyte.food_cmpd.sources.foodb import FoodbFoodCmpdSource
from phytebyte.bioactive_cmpd.sources import ChemblBioactiveCompoundSource
from phytebyte.bioactive_cmpd.target_input import GeneTargetsInput, CompoundNamesTargetInput, PhenotypesTargetInput
from phytebyte.fingerprinters import Fingerprinter
from phytebyte.cache import BitstringSmilesCache

import os
from tabulate import tabulate

FP_TYPE = "daylight"
SEED = .6  # Used to alter the negative_samples
chembl_db_url = os.environ['CHEMBL_DB_URL']
source = ChemblBioactiveCompoundSource(chembl_db_url, SEED)
# cache = BitstringSmilesCache.create("json", FP_TYPE)
# cache.load(FP_TYPE)
cache = None

target_input = GeneTargetsInput('agonist', ['PPARG'])

fingerprinter = Fingerprinter.create('daylight', cache)
pb = PhyteByte(source, target_input)
pb.set_negative_sampler('Tanimoto', fingerprinter)
pb.set_positive_clusterer('doesnt matter still', fingerprinter)
pb.set_fingerprinter(FP_TYPE, cache)
f1_scores = pb.train_and_evaluate('Random Forest',
                               neg_sample_size_factor=100,
                               true_threshold=.5)

# Now retrain and do the production run
pb.train('Random Forest', neg_sample_size_factor=100, true_threshold=.5)
food_cmpd_source = FoodbFoodCmpdSource(os.environ['FOODB_URL'])
food_cmpds_sorted = pb.sort_predicted_bioactive_food_cmpds(food_cmpd_source)
print("Classifying Food Compounds...")

pos_compound_bitarrays = [
    fingerprinter.fingerprint_and_encode(x.smiles, 'bitarray')
    for x in pb.load_positive_compounds('Random Forest')
]
rows = []
headers=["Compound", "Score", "Novel Relationship", "Foods"]
for i, (food_cmpd, score) in enumerate(food_cmpds_sorted[:100]):
    food_bullets = food_cmpd.get_food_bullets()
    if(len(food_bullets) > 0):
        in_training_data = fingerprinter.fingerprint_and_encode(
            food_cmpd.smiles, 'bitarray') in pos_compound_bitarrays
        rows.append([food_cmpd.name, score, not in_training_data, food_bullets])
print(tabulate(rows, headers=headers, tablefmt="grid"))
        

