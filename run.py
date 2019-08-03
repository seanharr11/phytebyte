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

target_input = GeneTargetsInput(['HMGCR'])


pb = PhyteByte(source, target_input)
pb.set_negative_sampler('Tanimoto', Fingerprinter.create('daylight', cache))
pb.set_positive_clusterer('doesnt matter still',
                          Fingerprinter.create('daylight', cache))
pb.set_fingerprinter(FP_TYPE, cache)
f1_scores = pb.evaluate_models('Random Forest',
                               neg_sample_size_factor=100,
                               true_threshold=.8)
food_cmpd_source = FoodbFoodCmpdSource(os.environ['FOODB_URL'])
food_cmpds_sorted = pb.sort_predicted_bioactive_food_cmpds(food_cmpd_source)
print("Classifying Food Compounds...")
for i, (food_cmpd, score) in enumerate(food_cmpds_sorted[:100]):
    food_info = food_cmpd.get_food_info_str(ignore_if_no_food=True,
                                            ignore_if_no_food_content=True)
    if food_info:
        print(f"{i}. ({score}) {food_info}")
