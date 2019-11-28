from phytebyte.bioactive_cmpd.sources.chembl import (ChemblBioactiveCompoundQuery)
from phytebyte.bioactive_cmpd.sources.chembl.bioactivity import antagonist_bioact_filter
import os
import pytest
from sqlalchemy import create_engine


@pytest.fixture
def cbc_hmgcr_query():
    q = ChemblBioactiveCompoundQuery(antagonist_bioact_filter, gene_tgts=['HMGCR'])
    return q

@pytest.fixture
def chembl_engine():
    e = create_engine(os.environ['CHEMBL_DB_URL'])
    return e


def test_run_query__executes(cbc_hmgcr_query, chembl_engine):
    sqla_q = cbc_hmgcr_query.build()
    chembl_engine.execute(sqla_q).fetchall()


def test_run_query__fetches_rows(cbc_hmgcr_query, chembl_engine):
    sqla_q = cbc_hmgcr_query.build()
    rows = chembl_engine.execute(sqla_q).fetchall()
    assert len(rows) > 0
