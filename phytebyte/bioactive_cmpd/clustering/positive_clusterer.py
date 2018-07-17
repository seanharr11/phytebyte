from typing import List
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

from phytebyte.bioactive_cmpd.types import BioactiveCompound
from phytebyte.fingerprinters.base import Fingerprinter
from .clusterer import Clusterer
from .cluster import Cluster


class PositiveClusterer(Clusterer):
    def __init__(self,
                 fingerprinter: Fingerprinter):
        self._fingerprinter = fingerprinter

    def run_dbscan(self, eps, pos_cmpd_nparrays):
        cluster_fit = DBSCAN(eps=eps).fit(pos_cmpd_nparrays)
        return cluster_fit.labels_

    def get_silhouette(self, labels, pos_cmpd_nparrays):
        try:
            ss = silhouette_score(pos_cmpd_nparrays, labels)
        except ValueError:
            # Silhouette score can't be generated from given labels
            # --> return a value below the possible true ss range
            ss = -2
        return ss

    def silhouette_series(self, eps_seq, pos_cmpd_nparrays):
        labels_seq = [self.run_dbscan(e, pos_cmpd_nparrays) for e in eps_seq]
        return np.array([self.get_silhouette(l, pos_cmpd_nparrays) for l in labels_seq])

    def find_clusters(self, 
                      pos_cmpds: List[BioactiveCompound],
                      eps_seq=np.array([0.1, 10, 15, 20, 100])):
        pos_cmpd_nparrays = self._fingerprinter.smiles_to_nparrays(
            [c.smiles for c in pos_cmpds])
        ss_seq = self.silhouette_series(eps_seq, pos_cmpd_nparrays)
        if np.max(ss_seq) < 0.5:
            # No silhouette score sufficient to warrant grouping
            return [Cluster(pos_cmpds)]
        elif (np.max(ss_seq) in ss_seq[[0, -1]]) & (np.max(ss_seq) != -2):
            # Raise error if max score is from an extreme epsilon value
            raise Exception("Silhouette optimal at an outlier epsilon value.")
        else:
            best_eps = eps_seq[np.where(ss_seq == np.max(ss_seq))][-1]
            # Arbitrarily choose the higher eps value if SSs are equal
            labels = self.run_dbscan(best_eps)
            return [Cluster(np.array(pos_cmpds)[labels == l])
                    for l in np.unique(labels)]
