# coding: utf-8
from phytebyte import PhyteByte
from phytebyte.food_cmpd.sources.foodb import FoodbFoodCmpdSource
from phytebyte.bioactive_cmpd.sources import ChemblBioactiveCompoundSource
from phytebyte.bioactive_cmpd.target_input import GeneTargetsInput, CompoundNamesTargetInput, PhenotypesTargetInput
from phytebyte.fingerprinters import Fingerprinter
from phytebyte.cache import BitstringSmilesCache

import os


FP_TYPE = "daylight"
chembl_db_url = os.environ['CHEMBL_DB_URL']
source = ChemblBioactiveCompoundSource(chembl_db_url)
# cache = BitstringSmilesCache.create("json", FP_TYPE)
# cache.load(FP_TYPE)
cache = None

target_input = GeneTargetsInput('agonist', ['PPARG'])


pb = PhyteByte(source, target_input)
pb.set_negative_sampler('Tanimoto', Fingerprinter.create('daylight', cache))
pb.set_positive_clusterer('doesnt matter still',
                          Fingerprinter.create('daylight', cache))
pb.set_fingerprinter(FP_TYPE, cache)
#f1_scores = pb.evaluate_models('Random Forest',
#                               neg_sample_size_factor=100,
#                               true_threshold=.5)

# Now retrain and do the production run
pb.train('Random Forest', neg_sample_size_factor=10, true_threshold=.5)
food_cmpd_source = FoodbFoodCmpdSource(os.environ['FOODB_URL'])
food_cmpds_sorted = pb.sort_predicted_bioactive_food_cmpds(food_cmpd_source)
print("Classifying Food Compounds...")

pos_compound_smiles = [x.smiles for x in pb.load_positive_compounds('Random Forest')]
for i, (food_cmpd, score) in enumerate(food_cmpds_sorted[:100]):
    food_info = food_cmpd.get_food_info_str(ignore_if_no_food=True,
                                            ignore_if_no_food_content=False)
    if food_info:
        if food_cmpd.smiles not in pos_compound_smiles:
            print(f"** {i}. ({score}) {food_info}")
        else:
            print(f"{i}. ({score}) {food_info}")

