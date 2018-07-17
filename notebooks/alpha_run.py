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

pb.train_model('Random Forest', 10)
food_cmpd_source = FoodbFoodCmpdSource(os.enviro['FOODB_URL'])
print(next(pb.sort_predicted_bioactive_food_cmpds(food_cmpd_source)))
