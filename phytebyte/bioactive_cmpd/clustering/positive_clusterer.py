from typing import List
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

from phytebyte.bioactive_cmpd.types import BioactiveCompound
from phytebyte.fingerprinters.base import Fingerprinter
from .clusterer import Clusterer


class PositiveClusterer(Clusterer):
    def __init__(self,
                 pos_cmpds: List[BioactiveCompound],
                 fingerprinter: Fingerprinter):
        self._pos_cmpds = pos_cmpds
        self._fingerprinter = fingerprinter
        self._data = self._fingerprinter.smiles_to_nparrays(
            [c.canonical_smiles for c in self._pos_cmpds])

    def run_dbscan(self, eps):
        cluster_fit = DBSCAN(eps=eps).fit(self._data)
        return cluster_fit.labels_

    def get_silhouette(self, labels):
        try:
            ss = silhouette_score(self._data, labels)
        except ValueError:
            # Silhouette score can't be generated from given labels
            # --> return a value below the possible true ss range
            ss = -2
        return ss

    def silhouette_series(self, eps_seq):
        labels_seq = [self.run_dbscan(e) for e in eps_seq]
        return np.array([self.get_silhouette(l) for l in labels_seq])

    def find_clusters(self, eps_seq=[0.1, 10, 15, 20, 100]):
        ss_seq = self.silhouette_series(eps_seq)
        if np.max(ss_seq) < 0.5:
            # No silhouette score sufficient to warrant grouping
            return [self._pos_cmpds]
        elif (np.max(ss_seq) in ss_seq[[0, -1]]) & (np.max(ss_seq) != -2):
            # Raise error if max score is from an extreme epsilon value
            raise Exception("Silhouette optimal at an outlier epsilon value.")
        else:
            max_idx = np.max(np.which(ss_seq == np.max(ss_seq)))
            labels = self.run_dbscan(eps_seq[max_idx])
            return [np.array(self._pos_cmpds)[labels == l] for l in
                    np.unique(labels)]
