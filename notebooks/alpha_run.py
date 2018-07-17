# coding: utf-8
from phytebyte import PhyteByte
from phytebyte.food_cmpd.sources.foodb import FoodbFoodCmpdSource
from phytebyte.bioactive_cmpd.sources import ChemblBioactiveCompoundSource
from phytebyte.bioactive_cmpd.target_input import GeneTargetsInput
from phytebyte.fingerprinters import Fingerprinter

import os


chembl_db_url = os.environ['CHEMBL_DB_URL']
source = ChemblBioactiveCompoundSource(chembl_db_url)
target_input = GeneTargetsInput(['HMGCR'])

pb = PhyteByte(source, target_input)
pb.set_negative_sampler('Tanimoto', Fingerprinter.create('daylight'))
pb.set_positive_clusterer('doesnt matter still',
                          Fingerprinter.create('daylight'))
pb.set_fingerprinter("daylight")
f1_scores = pb.evaluate_models('Random Forest',
                               neg_sample_size_factor=1,
                               true_threshold=.8)
print(f"F1: {f1_scores}")
food_cmpd_source = FoodbFoodCmpdSource(os.environ['FOODB_URL'])
food_cmpds_sorted = pb.sort_predicted_bioactive_food_cmpds(food_cmpd_source)
for i, food_cmpd in enumerate(food_cmpds_sorted[:25]):
    print(f"{i}. {str(food_cmpd)}")
