import os
import pickle


from phytebyte.bioactive_cmpd.sources import ChemblBioactiveCompoundSource


def test_cbc_source_is_picklable():
    cbc_source = ChemblBioactiveCompoundSource(os.environ['CHEMBL_DB_URL'])
    pickle.dumps(cbc_source)
