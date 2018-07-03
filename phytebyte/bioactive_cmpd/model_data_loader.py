import numpy as np
from typing import List

from phytebyte.bioactive_cmpd.sources.base import BioactiveCompoundSource
from phytebyte.bioactive_cmpd.negative_sampler import NegativeSampler
from phytebyte.bioactive_cmpd.positive_clusterer import (
    PositiveClusterer, FingerprintCluster)
from phytebyte.bioactive_cmpd import TargetInput
from phytebyte.bioactive_cmpd.types import ModelInputContainer


class ModelDataLoader():
    def __init__(self,
                 source: BioactiveCompoundSource,
                 negative_sampler: NegativeSampler,
                 positive_clusterer: PositiveClusterer,
                 target_input: TargetInput):
        self._source = source
        self._negative_sampler = negative_sampler
        self._positive_clusterer: positive_clusterer
        self._target_input = target_input

        self._pos_cmpd_clusters = None
        self._neg_cmpd_clusters = None

    def load(self, neg_sample_size_factor: int):
        assert isinstance(neg_sample_size_factor, int)
        pos_cmpds = self._target_input.fetch_bioactive_cmpds(
            self._source)
        # From this point forward pos_cmps exist as np.arrays in objs
        self._pos_cmpd_clusters = self._positive_clusterer.cluster(pos_cmpds)
        assert isinstance(self._pos_cmpd_clusters, FingerprintCluster)
        self._neg_cmpd_clusters = self._create_negative_cmpd_clusters(
            neg_sample_size_factor)
        assert isinstance(self._neg_cmpd_clusters, FingerprintCluster)

    def _create_negative_cmpd_clusters(self,
                                       neg_sample_size_factor: int) -> List[
                                            FingerprintCluster]:
        # We realize our Iterator into a List here...
        return [FingerprintCluster(
                    list(self._negative_sampler.sample(
                        [c.smiles for c in pos_cluster],
                        len(pos_cluster) * neg_sample_size_factor)))
                for pos_cluster in self._pos_cmpd_clusters]

    def split(self, test_size=.3, rand_state_seed=100):
        for clustr in self._pos_cmpd_clusters:
            clustr.split(test_size, rand_state_seed)
        for clustr in self._neg_cmpd_clusters:
            clustr.split(test_size, rand_state_seed)

    @property
    def positive_clusters(self):
        return self._pos_cmpd_clusters

    @property
    def model_data_containers(self) -> List[ModelInputContainer]:
        return [ModelInputContainer(
                    train_X=np.append(
                        pos_cluster.train,
                        neg_cluster.train),
                    train_y=np.append(
                        np.ones(len(pos_cluster.train)),
                        np.zeros(len(neg_cluster.train))),
                    test_X=np.append(
                        pos_cluster.test,
                        neg_cluster.test),
                    test_y=np.append(
                        np.ones(len(pos_cluster.test)),
                        np.zeros(len(neg_cluster.test))))
                for pos_cluster, neg_cluster in zip(
                    self._pos_cmpd_clusters,
                    self._neg_cmpd_clusters)]
