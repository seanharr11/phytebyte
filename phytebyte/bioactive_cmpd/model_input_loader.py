import logging
from typing import List, Iterator

from phytebyte.bioactive_cmpd.sources.base import BioactiveCompoundSource
from phytebyte.bioactive_cmpd.negative_samplers import NegativeSampler
from phytebyte.bioactive_cmpd.clustering import Clusterer, Cluster
from phytebyte.bioactive_cmpd.target_input import TargetInput
from phytebyte.fingerprinters import Fingerprinter
from phytebyte.modeling.input import (
    BinaryClassifierInputFactory, BinaryClassifierInput)


class ModelInputLoader():
    logger = logging.getLogger("ModelInputLoader")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '(%(asctime)s) - %(name)s [%(levelname)s]: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

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
    
    def load_positive_compounds(self):
        bioactive_cmpd_list = [lazy_cmpd_callable() for lazy_cmpd_callable in
                               self._target_input.fetch_bioactive_cmpds(
                                   self._source)]
        self._check_for_redundant_molregno(bioactive_cmpd_list)
        return bioactive_cmpd_list

    def load(self, neg_sample_size_factor: int,
             output_fingerprinter: Fingerprinter
             ) -> List[BinaryClassifierInput]:
        assert isinstance(neg_sample_size_factor, int)
        bioactive_cmpd_list = self.load_positive_compounds()
        self.logger.info(
            f"Found '{len(bioactive_cmpd_list)}' pos sample compounds.")
        self._pos_cmpd_clusters = self._positive_clusterer.find_clusters(
            bioactive_cmpd_list)
        self.logger.info(f"Found '{len(self._pos_cmpd_clusters)}' clusters.")
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
        
    @staticmethod
    def _check_for_redundant_molregno(bioactive_cmpd_list):
        all_molregno = [x.uid for x in bioactive_cmpd_list]
        distinct_molregno = set(all_molregno)
        if len(distinct_molregno) < len(all_molregno):
            raise Exception(f"'{len(distinct_molregno)}' distinct compounds, '{len(all_molregno)}' total compounds.")

    def _get_neg_bioactive_cmpd_iters(self,
                                      neg_sample_size_factor: int,
                                      output_fingerprinter: Fingerprinter
                                      ) -> List[Iterator]:
        return [self._negative_sampler.sample(
                   [cmpd.smiles for cmpd in clust.bioactive_cmpds],
                   len(clust.bioactive_cmpds) * neg_sample_size_factor,
                   output_fingerprinter,
                   self._encoding)
                for clust in self._pos_cmpd_clusters]

    def _create_binary_classifier_input(self,
                                        cluster: Cluster,
                                        neg_cmpd_iter: Iterator,
                                        output_fingerprinter: Fingerprinter
                                        ) -> BinaryClassifierInput:
        neg_cmpds = list(neg_cmpd_iter)
        self.logger.info(f"Found '{len(neg_cmpds)}' neg samples")
        pos_cmpds = cluster.get_encoded_cmpds(self._encoding,
                                              output_fingerprinter)
        self.logger.info(f"Found '{len(pos_cmpds)}' pos samples")
        return BinaryClassifierInputFactory.create(
            encoding=self._encoding,
            positives=pos_cmpds,
            negatives=neg_cmpds)

    @property
    def positive_clusters(self):
        return self._pos_cmpd_clusters
