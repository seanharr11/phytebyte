from bitarray import bitarray
import numpy as np


class MockFingerprinter(object):
    smile_to_fp_dict = {
        "CO=N2": bitarray("011" * 341 + "1"),
        # Should yield Tanimoto's of .67
        "C=N": bitarray("01" * 512),
        # Tanimotos of .5
        "C": bitarray("1" * 1024)
        # Tanimotos of 1.0
    }

    def __init__(self):
        self.call_arg_ls = []

    def smiles_to_bitarray(self, smile):
        self.call_arg_ls.append((smile,))
        return self.smile_to_fp_dict[smile]

    def bitarray_to_nparray(self, bitarr):
        return np.array(bitarr.tolist())


class MockBioactiveCmpdSource(object):
    def __init__(self):
        self._count = 0
        self.call_args_ls = []

    def fetch_random_compounds_exc_smiles(self, excluded_smiles, limit):
        self.call_args_ls.append((excluded_smiles, limit,))
        for i in range(limit):
            self._count += 1
            yield "C"
