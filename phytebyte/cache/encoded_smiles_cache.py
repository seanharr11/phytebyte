from abc import ABC, abstractmethod
import os
import pickle
import redis
from typing import List

from phytebyte import ROOT_DIR
from phytebyte.fingerprinters import Fingerprinter


class EncodedSmilesCache(ABC, object):
    @abstractmethod
    def get(smiles: List[str], fp_type: str, encoding: str):
        """ Given a smiles string, a fingerprint type, and a request encoding, retrieve
        the fingerprints encoding associated with the provided smiles.
        """
        pass

    @abstractmethod
    def update(smiles: List[str], fingerprinter: Fingerprinter):
        """ Given a smiles string and a fingerprinter, generate the encoding
        and store it in the relevant data object or database.
        """
        pass

    @abstractmethod
    def write():
        """ Some cache types (e.g. Python objects) may need to be explicitly
        written after being updated, while others (e.g. databases) may not. If
        needed, write the file here, otherwise pass.
        """
        pass

    @abstractmethod
    def clear():
        """ Clear the current cache. """
        pass


class DictEncodedSmilesCache(EncodedSmilesCache):
    def __init__(self, root_dir=ROOT_DIR):
        self._root_dir = root_dir
        self._cache = {}

    def load(self, fp_type, encoding):
        filename = f'{fp_type}_{encoding}.pkl'
        filepath = f'{self._root_dir}/.cache/{filename}'
        with open(filepath, 'rb') as f:
            if filename not in os.listdir(f'{self._root_dir}/.cache'):
                print("Cache has not been created for this fingerprint"
                      "and encoding combination.")
                self._cache = {}
            else:
                self._cache[f"{fp_type}_{encoding}"] = pickle.load(f)

    def get(self, smiles, fp_type, encoding):
        return self._cache[f"{fp_type}_{encoding}"].get(smiles)

    def update(self, smiles, fingerprinter, encoding):
        enc = fingerprinter.fingerprint_and_encode(smiles, encoding)
        self._cache[f"{fingerprinter.fp_type}_{encoding}"][smiles] = enc

    def write(self):
        for filename in self._cache.keys():
            with open(f"{self._root_dir}/.cache/{filename}.pkl", 'wb') as f:
                pickle.dump(self._cache[filename], f)

    def clear(self):
        self._cache = {}


class RedisEncodedSmilesCache(EncodedSmilesCache):
    def __init__(self, root_dir=ROOT_DIR):
        self._root_dir = root_dir
        self._redis = None

    def connect(self, fp_type, encoding):
        print(f"Connecting to redis (pid: {os.getpid()})")
        self._redis = redis.StrictRedis(host='localhost', port=8888)

    def disconnect(self):
        print(f"Disconnecting from redis (pid: {os.getpid()})")
        # https://stackoverflow.com/questions/24875806/redis-in-python-how-do-you-close-the-connection
        del self._redis
        self._redis = None

    def get(self, smiles, fp_type, encoding):
        if self._redis is None:
            self.connect(fp_type, encoding)
        encoded_cmpd = self._redis.get(f'{fp_type}_{encoding}_{smiles}')
        return pickle.loads(encoded_cmpd) if encoded_cmpd else None

    def update(self, smiles, fingerprinter, encoding):
        if self._redis is None:
            self.connect(fingerprinter.fp_type, encoding)
        enc = fingerprinter.fingerprint_and_encode(smiles, encoding)
        return self._redis.set(f'{fingerprinter.fp_type}_{encoding}_{smiles}',
                               pickle.dumps(enc))

    def write(self):
        self._redis.save()

    def clear(self):
        raise NotImplemented
