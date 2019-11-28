import os
import pickle


from phytebyte.bioactive_cmpd.sources import ChemblBioactiveCompoundSource 
from phytebyte.fingerprinters import Fingerprinter

def test_cbc_source_is_picklable():
    cbc_source = ChemblBioactiveCompoundSource(os.environ['CHEMBL_DB_URL'])
    pickle.dumps(cbc_source)


def test_cbc_source__neg_cmpd_query_is_reproducible():
    
    cbc_source = ChemblBioactiveCompoundSource(os.environ['CHEMBL_DB_URL'])
    fp = Fingerprinter.create('daylight')
    
    neg_cmpds_1 = cbc_source.fetch_random_compounds_exc_smiles([], 500)
    neg_cmpds_2 = cbc_source.fetch_random_compounds_exc_smiles([], 500)
    
    fps_1 = [fp.fingerprint_and_encode(cmpd, 'numpy').sum()
           for cmpd in neg_cmpds_1]
    fps_2 = [fp.fingerprint_and_encode(cmpd, 'numpy').sum()
           for cmpd in neg_cmpds_2]
    assert(len(fps_1) == len(fps_2))
    assert(fps_1 == fps_2)

