from abc import abstractmethod, ABC
from sqlalchemy import select, and_, not_, func
from typing import List

from phytebyte.drug.types import (
    BioactiveCompound, CompoundBioactivity, BioactivityStandardFilter)
from .models import (
    CompoundStructure, MoleculeDictionary, ComponentSynonym,
    ComponentRecord, Activity, Assay, ComponentSequence, TargetComponent,
    CompoundRecord, TargetDictionary
)

default_bioact_filter = BioactivityStandardFilter(
    types=['IC50', 'EC50', 'AC50', 'GI50'],
    relations=['=', '<'],
    units=['nM'],
    min_value=20000)


class Query(ABC):
    def __str__(self):
        return self.build().compile(compile_kwargs={"literal_binds": True})

    def __repr__(self):
        return str(self)

    def build(self) -> select:
        query = self._select\
                    .select_from(self._select_from)\
                    .where(self._whereclause)\
                    .order_by(self._order_by)\
                    .group_by(*self._group_by)
        return query

    @property
    @abstractmethod
    def _select(self):
        pass

    @property
    @abstractmethod
    def _select_from(self):
        pass

    @property
    def _whereclause(self):
        return True

    @property
    def _order_by(self):
        return None

    @property
    def _group_by(self):
        return None

    @property
    def _having(self):
        return None


class ChemblBioactiveCompoundQuery(Query):
    def __init__(self,
                 bioact_standard_filter=default_bioact_filter,
                 gene_tgts: List[str]=None,
                 compound_names: List[str]=None):
        self._bioact_standard_filter = bioact_standard_filter
        assert isinstance(self.gene_tgts, (list, tuple))
        self._gene_tgts = gene_tgts
        assert isinstance(self.compound_names, (list, tuple))
        self._compound_names = compound_names

    def __repr__(self):
        return f"""<ChemblBioactiveCompoundQuery
           {self.bioact_standard_filter},
           {self.gene_tgts},
           {self.compound_names}>"""

    @staticmethod
    def row_to_bioactive_compound(row) -> BioactiveCompound:
        return BioactiveCompound(
            uid=row[0], pref_name=row[1], canonical_smiles=row[2],
            gene_target=row[3], name=row[4],
            bioactivities=[CompoundBioactivity(*bioact_tup)
                           for bioact_tup in zip(row[5:9])])

    @property
    def _select(self):
        return select([
            CompoundStructure.molregno.label("uid"),
            MoleculeDictionary.pref_name.label("pref_name"),
            CompoundStructure.canonical_smiles.label("canonical_smiles"),
            ComponentSynonym.component_synonym.label("gene_target"),
            ComponentRecord.compound_name.label("name"),
            func.array_agg(Activity.standard_value).label("value_arr"),
            func.array_agg(Activity.standard_units).label("units_arr"),
            func.array_agg(Activity.standard_type).label("type_arr"),
            func.array_agg(Assay.description).label("descr_arr")])

    @property
    def _select_from(self):
        return (
            ComponentSynonym
            .join(ComponentSequence,
                  ComponentSequence.component_id ==
                  ComponentSynonym.component_id)
            .join(TargetComponent,
                  TargetComponent.component_id ==
                  ComponentSequence.component_id)
            .join(TargetDictionary,
                  TargetDictionary.tid == TargetComponent.tid)
            .join(Assay,
                  Assay.tid == TargetDictionary.tid)
            .join(Activity,
                  Activity.assay_id == Assay.assay_id)
            .join(CompoundRecord,
                  CompoundRecord.record_id == Activity.record_id)
            .join(MoleculeDictionary,
                  MoleculeDictionary.molregno == CompoundRecord.molregno)
            .join(CompoundStructure,
                  CompoundStructure.molregno == MoleculeDictionary.molregno))

    @property
    def _whereclause(self):
        and_tuple = (
            ComponentSynonym.syn_type == "GENE_SYMBOL",
            ComponentSequence.organism == "Homo sapiens",
            Assay.confidence_score >= 7,
            Activity.standard_type.in_(self._bioact_standard_filter.types),
            Activity.standard_relation.in_(
                self._bioact_standard_filter.relations),
            Activity.standard_units.in_(
                self._bioact_standard_filter.units),
            Activity.standard_value > self._bioact_standard_filter.mine_value)
        if self.gene_tgts:
            and_tuple += ComponentSynonym.component_synonym.in_(
                self._gene_tgts)
        if self.compound_names:
            and_tuple += CompoundRecord.compound_name.in_(self._compound_names)
        return and_(and_tuple)

    @property
    def _group_by(self):
        group_by_tuple = (
            CompoundStructure.molregno,
            MoleculeDictionary.molregno,
            ComponentSynonym.component_synonym,
            CompoundRecord.compound_name)
        return group_by_tuple


class ChemblRandomCompoundSmilesQuery():
    def __init__(self, limit: int, excluded_smiles: List[str]):
        self._limit = limit
        self._excluded_smiles = excluded_smiles

    def __repr__(self):
        return f"""<ChemblRandomCompoundSmilesQuery
           Limit: {self.limit}>"""

    def __str__(self):
        return self.build().compile(compile_kwargs={"literal_binds": True})

    @property
    def _select(self):
        return select([CompoundStructure.canonical_smiles]).distinct()

    @property
    def _select_from(self):
        return CompoundStructure

    @property
    def _whereclause(self):
        return not_(
            CompoundStructure.canonical_smiles.in_(self._excluded_smiles))

    @property
    def _order_by(self):
        return func.random()
