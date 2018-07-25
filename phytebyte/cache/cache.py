import pickle

from phytebyte.fingerprinters import Fingerprinter
from phytebyte.food_cmpd.sources import FoodCmpdSource
from phytebyte.bioactive_cmpd import BioactiveCompoundSource
from phytebyte import ROOT_DIR


def _get_all_cmpds(cmpd_source):
    if isinstance(cmpd_source, FoodCmpdSource):
        return cmpd_source.fetch_all_cmpds()
    elif isinstance(cmpd_source, BioactiveCompoundSource):
        return cmpd_source.fetch_random_compounds_exc_smiles([], 100)


def _get_cmpd_type(cmpd_source):
    if isinstance(cmpd_source, FoodCmpdSource):
        return 'foodcmpds'
    elif isinstance(cmpd_source, BioactiveCompoundSource):
        return 'bioactivecmpds'


def save(cmpd_source, fingerprinter: Fingerprinter, encoding):
        all_cmpds = _get_all_cmpds(cmpd_source)
        all_encoded_fps = [fingerprinter.fingerprint_and_encode(
            c.smiles, encoding) for c in all_cmpds]
        filename = '_'.join(_get_cmpd_type(cmpd_source),
                            fingerprinter.__class__.__name__,
                            encoding) + '.pkl'
        filepath = f'{ROOT_DIR}/.cache/{filename}'
        with open(filepath, 'wb') as f:
            pickle.dump(all_encoded_fps, f) 
        return None


def load(cmpd_source, fingerprinter: Fingerprinter, encoding):
    filename = '_'.join(_get_cmpd_type(cmpd_source),
                        fingerprinter.__class__.__name__,
                        encoding) + '.pkl'
    # filename = f'foodcmpd_{fingerprinter.__class__.__name__}_{encoding}.pkl'
    filepath = f'{ROOT_DIR}/.cache/{filename}'
    with open(filepath, 'rb') as f:
        fps = pickle.load(f)
    return (fp for fp in fps)
