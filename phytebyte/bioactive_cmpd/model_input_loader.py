from typing import List, Iterator

from phytebyte.bioactive_cmpd.sources.base import BioactiveCompoundSource
from phytebyte.bioactive_cmpd.negative_samplers import NegativeSampler
from phytebyte.bioactive_cmpd.clustering import Clusterer, Cluster
from phytebyte.bioactive_cmpd.target_input import TargetInput
from phytebyte.fingerprinters import Fingerprinter
from phytebyte.modeling.input import (
    BinaryClassifierInputFactory, BinaryClassifierInput)


class ModelInputLoader():
    def __init__(self,
                 source: BioactiveCompoundSource,
                 negative_sampler: NegativeSampler,
                 positive_clusterer: Clusterer,
                 target_input: TargetInput,
                 encoding: str):
        self._source = source
        self._negative_sampler = negative_sampler
        self._positive_clusterer = positive_clusterer
        self._target_input = target_input
        self._encoding = encoding

        self._pos_cmpd_clusters = None
        self._neg_cmpd_iters = None

    def load(self, neg_sample_size_factor: int,
             output_fingerprinter: Fingerprinter
             ) -> List[BinaryClassifierInput]:
        assert isinstance(neg_sample_size_factor, int)
        bioactive_cmpd_list = [lazy_cmpd_callable() for lazy_cmpd_callable in
                               self._target_input.fetch_bioactive_cmpds(
                                   self._source)]
        self._pos_cmpd_clusters = self._positive_clusterer.find_clusters(
            bioactive_cmpd_list)
        self._negative_sampler.set_sample_encoding(self._encoding)
        self._neg_cmpd_iters = self._get_neg_bioactive_cmpd_iters(
            neg_sample_size_factor,
            output_fingerprinter)
        # Iterators turned into List below!
        model_inputs = [
            self._create_binary_classifier_input(clust, neg_cmpd_iter,
                                                 output_fingerprinter)
            for clust, neg_cmpd_iter in zip(
                self._pos_cmpd_clusters, self._neg_cmpd_iters)]
        return model_inputs

    def _get_neg_bioactive_cmpd_iters(self,
                                      neg_sample_size_factor: int,
                                      output_fingerprinter: Fingerprinter
                                      ) -> List[Iterator]:
        return [self._negative_sampler.sample(
                   [cmpd.smiles for cmpd in clust.bioactive_cmpds],
                   len(clust.bioactive_cmpds) * neg_sample_size_factor,
                   output_fingerprinter)
                for clust in self._pos_cmpd_clusters]

    def _create_binary_classifier_input(self,
                                        cluster: Cluster,
                                        neg_cmpd_iter: Iterator,
                                        output_fingerprinter: Fingerprinter
                                        ) -> BinaryClassifierInput:
        return BinaryClassifierInputFactory.create(
            encoding=self._encoding,
            positives=cluster.get_encoded_cmpds(self._encoding,
                                                output_fingerprinter),
            negatives=list(neg_cmpd_iter))

    @property
    def positive_clusters(self):
        return self._pos_cmpd_clusters
