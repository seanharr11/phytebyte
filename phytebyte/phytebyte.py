from .bioactive_cmpd.negative_samplers import NegativeSampler
from .bioactive_cmpd.clustering import Clusterer
from .bioactive_cmpd.target_input import TargetInput
from .bioactive_cmpd.sources import BioactiveCompoundSource
from .bioactive_cmpd import ModelInputLoader
from .modeling.models import BinaryClassifierModel
from .food_cmpd import FoodCmpdSource, FoodCmpd
from .fingerprinters import Fingerprinter

from typing import List, Iterator, Tuple


class PhyteByte():
    def __init__(self, config_file_path: str=None):
        self.model = None
        self._config_file_path = config_file_path
        self._negative_sampler = None
        self._positive_clusterer = None
        self._target_input = None
        self._source = None
        self._fingerprinter = None

        if config_file_path:
            self._load_config()

    def _load_config(self):
        raise NotImplementedError

    def set_negative_sampler(self, negative_sampler_name: str,
                             *args, **kwargs):
        self._negative_sampler = NegativeSampler.create(
            negative_sampler_name, *args, **kwargs)

    def set_positive_clusterer(self, clusterer_name: str, *args, **kwargs):
        self._positive_clusterer = Clusterer.create(
            clusterer_name, *args, **kwargs)

    def set_fingerprinter(self, fingerprinter_name: str):
        self._fingerprinter = Fingerprinter.create(fingerprinter_name)

    def set_target_input(self, target_input: TargetInput):
        self._target_input = target_input

    def set_source(self, source: BioactiveCompoundSource):
        self._source = source

    def train_model(self,
                    model_type: str,
                    neg_sample_size: int,
                    *args,
                    **kwargs):
        binary_classifier_model = BinaryClassifierModel.create(model_type)
        mdl = ModelInputLoader(self._source, self._negative_sampler,
                               self._positive_clusterer, self._target_input,
                               binary_classifier_model.expected_encoding)
        binary_classifier_input = mdl.load(
            neg_sample_size, self._fingerprinter)
        binary_classifier_model.train(binary_classifier_input, *args, **kwargs)
        self.model = binary_classifier_model

    def predict_bioactive_food_cmpd_iter(self,
                                         food_cmpd_source: FoodCmpdSource
                                         ) -> Iterator[Tuple[FoodCmpd, float]]:
        food_cmpd_iter = food_cmpd_source.fetch_all_cmpds()
        for food_cmpd in food_cmpd_iter:
            encoded_cmpd = self._fingerprinter.fingerprint_and_encode(
                food_cmpd.smiles, self.model.exepected_encoding)
            yield food_cmpd, self.model.calc_score(encoded_cmpd)

    def sort_predicted_bioactive_food_cmpds(self, food_cmpd_source:
                                            FoodCmpdSource
                                            ) -> List[Tuple[FoodCmpd, float]]:
        return sorted(self.predict_bioactive_food_cmpd_iter(food_cmpd_source),
                      key=lambda tup: tup[1],
                      reverse=True)
