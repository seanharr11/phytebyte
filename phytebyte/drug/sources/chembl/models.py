# coding: utf-8
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Table,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


t_action_type = Table(
    "action_type",
    metadata,
    Column("action_type", String(50), nullable=False, index=True),
    Column("description", String(200), nullable=False),
    Column("parent_type", String(50)),
)


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint(
            "(potential_duplicate = ANY (ARRAY[0, 1])) OR "
            "(potential_duplicate IS NULL)"
        ),
        CheckConstraint(
            "(standard_flag = ANY (ARRAY[0, 1])) OR (standard_flag IS NULL)"
        ),
    )

    activity_id = Column(BigInteger, primary_key=True)
    assay_id = Column(
        ForeignKey("assays.assay_id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    doc_id = Column(
        ForeignKey("docs.doc_id", deferrable=True, initially="DEFERRED"),
        index=True,
    )
    record_id = Column(
        ForeignKey(
            "compound_records.record_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    standard_relation = Column(String(50), index=True)
    published_value = Column(Numeric, index=True)
    published_units = Column(String(100), index=True)
    standard_value = Column(Numeric, index=True)
    standard_units = Column(String(100), index=True)
    standard_flag = Column(SmallInteger)
    standard_type = Column(String(250), index=True)
    activity_comment = Column(String(4000))
    published_type = Column(String(250), index=True)
    data_validity_comment = Column(
        ForeignKey(
            "data_validity_lookup.data_validity_comment",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    potential_duplicate = Column(SmallInteger)
    published_relation = Column(String(50), index=True)
    pchembl_value = Column(Numeric(4, 2), index=True)
    bao_endpoint = Column(
        ForeignKey(
            "bioassay_ontology.bao_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    uo_units = Column(String(10))
    qudt_units = Column(String(70))

    assay = relationship("Assay")
    bioassay_ontology = relationship("BioassayOntology")
    data_validity_lookup = relationship("DataValidityLookup")
    doc = relationship("Doc")
    molecule_dictionary = relationship("MoleculeDictionary")
    record = relationship("CompoundRecord")


class LigandEff(Activity):
    __tablename__ = "ligand_eff"
    __table_args__ = (
        CheckConstraint("bei >= (0)::numeric"),
        CheckConstraint("le >= (0)::numeric"),
        CheckConstraint("sei >= (0)::numeric"),
    )

    activity_id = Column(
        ForeignKey(
            "activities.activity_id", deferrable=True, initially="DEFERRED"
        ),
        primary_key=True,
    )
    bei = Column(Numeric(9, 2))
    sei = Column(Numeric(9, 2))
    le = Column(Numeric(9, 2))
    lle = Column(Numeric(9, 2))


class ActivityStdsLookup(Base):
    __tablename__ = "activity_stds_lookup"
    __table_args__ = (UniqueConstraint("standard_type", "standard_units"),)

    std_act_id = Column(Integer, primary_key=True)
    standard_type = Column(String(250), nullable=False)
    definition = Column(String(500))
    standard_units = Column(String(100), nullable=False)
    normal_range_min = Column(Numeric(24, 12))
    normal_range_max = Column(Numeric(24, 12))


class AssayParameter(Base):
    __tablename__ = "assay_parameters"
    __table_args__ = (UniqueConstraint("assay_id", "parameter_type"),)

    assay_param_id = Column(Integer, primary_key=True)
    assay_id = Column(
        ForeignKey("assays.assay_id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    parameter_type = Column(
        ForeignKey(
            "parameter_type.parameter_type",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    parameter_value = Column(String(2000), nullable=False)

    assay = relationship("Assay")
    parameter_type1 = relationship("ParameterType")


class AssayType(Base):
    __tablename__ = "assay_type"

    assay_type = Column(String(1), primary_key=True, index=True)
    assay_desc = Column(String(250))


class Assay(Base):
    __tablename__ = "assays"
    __table_args__ = (
        CheckConstraint(
            "(assay_category)::text = ANY "
            "(ARRAY[('screening'::character varying)::text,"
            " ('panel'::character varying)::text, "
            "('confirmatory'::character varying)::text, "
            "('summary'::character varying)::text, "
            "('other'::character varying)::text])"
        ),
        CheckConstraint(
            "(assay_test_type)::text = ANY "
            "(ARRAY[('In vivo'::character varying)::text,"
            "('In vitro'::character varying)::text,"
            "('Ex vivo'::character varying)::text])"
        ),
        CheckConstraint("assay_tax_id >= 0"),
        CheckConstraint("confidence_score >= 0"),
        CheckConstraint("variant_id >= 0"),
    )

    assay_id = Column(Integer, primary_key=True)
    doc_id = Column(
        ForeignKey("docs.doc_id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    description = Column(String(4000))
    assay_type = Column(
        ForeignKey(
            "assay_type.assay_type", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    assay_test_type = Column(String(20))
    assay_category = Column(String(20))
    assay_organism = Column(String(250))
    assay_tax_id = Column(BigInteger)
    assay_strain = Column(String(200))
    assay_tissue = Column(String(100))
    assay_cell_type = Column(String(100))
    assay_subcellular_fraction = Column(String(100))
    tid = Column(
        ForeignKey(
            "target_dictionary.tid", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    relationship_type = Column(
        ForeignKey(
            "relationship_type.relationship_type",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    confidence_score = Column(
        ForeignKey(
            "confidence_score_lookup.confidence_score",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    curated_by = Column(
        ForeignKey(
            "curation_lookup.curated_by", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    src_id = Column(
        ForeignKey("source.src_id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    src_assay_id = Column(String(50))
    chembl_id = Column(
        ForeignKey(
            "chembl_id_lookup.chembl_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        unique=True,
    )
    cell_id = Column(
        ForeignKey(
            "cell_dictionary.cell_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    bao_format = Column(
        ForeignKey(
            "bioassay_ontology.bao_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    tissue_id = Column(
        ForeignKey(
            "tissue_dictionary.tissue_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    variant_id = Column(
        ForeignKey(
            "variant_sequences.variant_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )

    assay_type1 = relationship("AssayType")
    bioassay_ontology = relationship("BioassayOntology")
    cell = relationship("CellDictionary")
    chembl = relationship("ChemblIdLookup", uselist=False)
    confidence_score_lookup = relationship("ConfidenceScoreLookup")
    curation_lookup = relationship("CurationLookup")
    doc = relationship("Doc")
    relationship_type1 = relationship("RelationshipType")
    src = relationship("Source")
    target_dictionary = relationship("TargetDictionary")
    tissue = relationship("TissueDictionary")
    variant = relationship("VariantSequence")


class AtcClassification(Base):
    __tablename__ = "atc_classification"

    who_name = Column(String(150))
    level1 = Column(String(10))
    level2 = Column(String(10))
    level3 = Column(String(10))
    level4 = Column(String(10))
    level5 = Column(String(10), primary_key=True, index=True)
    level1_description = Column(String(150))
    level2_description = Column(String(150))
    level3_description = Column(String(150))
    level4_description = Column(String(150))


class BindingSite(Base):
    __tablename__ = "binding_sites"

    site_id = Column(Integer, primary_key=True)
    site_name = Column(String(200))
    tid = Column(
        ForeignKey(
            "target_dictionary.tid", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )

    target_dictionary = relationship("TargetDictionary")


class BioComponentSequence(Base):
    __tablename__ = "bio_component_sequences"
    __table_args__ = (CheckConstraint("tax_id >= 0"),)

    component_id = Column(Integer, primary_key=True)
    component_type = Column(String(50), nullable=False)
    description = Column(String(200))
    sequence = Column(Text)
    sequence_md5sum = Column(String(32))
    tax_id = Column(BigInteger)
    organism = Column(String(150))


class BioassayOntology(Base):
    __tablename__ = "bioassay_ontology"

    bao_id = Column(String(11), primary_key=True, index=True)
    label = Column(String(100), nullable=False)


class BiotherapeuticComponent(Base):
    __tablename__ = "biotherapeutic_components"
    __table_args__ = (UniqueConstraint("molregno", "component_id"),)

    biocomp_id = Column(Integer, primary_key=True)
    molregno = Column(
        ForeignKey(
            "biotherapeutics.molregno", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    component_id = Column(
        ForeignKey(
            "bio_component_sequences.component_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )

    component = relationship("BioComponentSequence")
    biotherapeutic = relationship("Biotherapeutic")


class CellDictionary(Base):
    __tablename__ = "cell_dictionary"
    __table_args__ = (
        CheckConstraint("cell_source_tax_id >= 0"),
        UniqueConstraint("cell_name", "cell_source_tax_id"),
    )

    cell_id = Column(Integer, primary_key=True)
    cell_name = Column(String(50), nullable=False)
    cell_description = Column(String(200))
    cell_source_tissue = Column(String(50))
    cell_source_organism = Column(String(150))
    cell_source_tax_id = Column(BigInteger)
    clo_id = Column(String(11))
    efo_id = Column(String(12))
    cellosaurus_id = Column(String(15))
    cl_lincs_id = Column(String(8))
    chembl_id = Column(
        ForeignKey(
            "chembl_id_lookup.chembl_id", deferrable=True, initially="DEFERRED"
        ),
        unique=True,
    )

    chembl = relationship("ChemblIdLookup", uselist=False)


class ChemblIdLookup(Base):
    __tablename__ = "chembl_id_lookup"
    chembl_id = Column(String(20), primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)
    status = Column(
        String(10),
        nullable=False,
        server_default=text("'ACTIVE'::character varying"),
    )


class ComponentClas(Base):
    __tablename__ = "component_class"
    __table_args__ = (UniqueConstraint("component_id", "protein_class_id"),)

    component_id = Column(
        ForeignKey(
            "component_sequences.component_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    protein_class_id = Column(
        ForeignKey(
            "protein_classification.protein_class_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    comp_class_id = Column(Integer, primary_key=True)

    component = relationship("ComponentSequence")
    protein_class = relationship("ProteinClassification")


class ComponentDomain(Base):
    __tablename__ = "component_domains"
    __table_args__ = (
        CheckConstraint("end_position >= 0"),
        CheckConstraint("start_position >= 0"),
        UniqueConstraint("domain_id", "component_id", "start_position"),
    )

    compd_id = Column(Integer, primary_key=True)
    domain_id = Column(
        ForeignKey("domains.domain_id", deferrable=True, initially="DEFERRED"),
        index=True,
    )
    component_id = Column(
        ForeignKey(
            "component_sequences.component_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    start_position = Column(Integer)
    end_position = Column(Integer)

    component = relationship("ComponentSequence")
    domain = relationship("Domain")


class ComponentGo(Base):
    __tablename__ = "component_go"
    __table_args__ = (UniqueConstraint("component_id", "go_id"),)

    comp_go_id = Column(Integer, primary_key=True)
    component_id = Column(
        ForeignKey(
            "component_sequences.component_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    go_id = Column(
        ForeignKey(
            "go_classification.go_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )

    component = relationship("ComponentSequence")
    go = relationship("GoClassification")


class ComponentSequence(Base):
    __tablename__ = "component_sequences"
    __table_args__ = (
        CheckConstraint(
            "(component_type)::text = ANY (ARRAY[('PROTEIN'::character varying)::text, ('DNA'::character varying)::text, ('RNA'::character varying)::text])"
        ),
        CheckConstraint(
            "(db_source)::text = ANY (ARRAY[('SWISS-PROT'::character varying)::text, ('TREMBL'::character varying)::text, ('Manual'::character varying)::text])"
        ),
        CheckConstraint("tax_id >= 0"),
    )

    component_id = Column(Integer, primary_key=True)
    component_type = Column(String(50))
    accession = Column(String(25), unique=True)
    sequence = Column(Text)
    sequence_md5sum = Column(String(32))
    description = Column(String(200))
    tax_id = Column(BigInteger)
    organism = Column(String(150))
    db_source = Column(String(25))
    db_version = Column(String(10))


class ComponentSynonym(Base):
    __tablename__ = "component_synonyms"
    __table_args__ = (
        CheckConstraint(
            "(syn_type)::text = ANY (ARRAY[('HGNC_SYMBOL'::character varying)::text, ('GENE_SYMBOL'::character varying)::text, ('UNIPROT'::character varying)::text, ('MANUAL'::character varying)::text, ('OTHER'::character varying)::text, ('EC_NUMBER'::character varying)::text])"
        ),
        UniqueConstraint("component_id", "component_synonym", "syn_type"),
    )

    compsyn_id = Column(Integer, primary_key=True)
    component_id = Column(
        ForeignKey(
            "component_sequences.component_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    component_synonym = Column(String(500))
    syn_type = Column(String(20))

    component = relationship("ComponentSequence")


class CompoundRecord(Base):
    __tablename__ = "compound_records"

    record_id = Column(Integer, primary_key=True)
    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    doc_id = Column(
        ForeignKey("docs.doc_id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    compound_key = Column(String(250), index=True)
    compound_name = Column(String(4000))
    src_id = Column(
        ForeignKey("source.src_id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    src_compound_id = Column(String(150), index=True)

    doc = relationship("Doc")
    molecule_dictionary = relationship("MoleculeDictionary")
    src = relationship("Source")


class CompoundStructuralAlert(Base):
    __tablename__ = "compound_structural_alerts"
    __table_args__ = (
        CheckConstraint("alert_id >= 0"),
        CheckConstraint("cpd_str_alert_id >= 0"),
        UniqueConstraint("molregno", "alert_id"),
    )

    cpd_str_alert_id = Column(Integer, primary_key=True)
    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    alert_id = Column(
        ForeignKey(
            "structural_alerts.alert_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )

    alert = relationship("StructuralAlert")
    molecule_dictionary = relationship("MoleculeDictionary")


class ConfidenceScoreLookup(Base):
    __tablename__ = "confidence_score_lookup"
    __table_args__ = (CheckConstraint("confidence_score >= 0"),)

    confidence_score = Column(SmallInteger, primary_key=True)
    description = Column(String(100), nullable=False)
    target_mapping = Column(String(30), nullable=False)


class CurationLookup(Base):
    __tablename__ = "curation_lookup"

    curated_by = Column(String(32), primary_key=True, index=True)
    description = Column(String(100), nullable=False)


class DataValidityLookup(Base):
    __tablename__ = "data_validity_lookup"

    data_validity_comment = Column(String(30), primary_key=True, index=True)
    description = Column(String(200))


class DefinedDailyDose(Base):
    __tablename__ = "defined_daily_dose"
    __table_args__ = (
        CheckConstraint(
            "(ddd_units)::text = ANY (ARRAY[('LSU'::character varying)::text, ('MU'::character varying)::text, ('TU'::character varying)::text, ('U'::character varying)::text, ('g'::character varying)::text, ('mcg'::character varying)::text, ('mg'::character varying)::text, ('ml'::character varying)::text, ('mmol'::character varying)::text, ('tablet'::character varying)::text])"
        ),
        CheckConstraint("ddd_value >= (0)::numeric"),
    )

    atc_code = Column(
        ForeignKey(
            "atc_classification.level5", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    ddd_value = Column(Numeric(9, 2))
    ddd_units = Column(String(200))
    ddd_admr = Column(String(1000))
    ddd_comment = Column(String(2000))
    ddd_id = Column(Integer, primary_key=True)

    atc_classification = relationship("AtcClassification")


class Doc(Base):
    __tablename__ = "docs"
    __table_args__ = (
        CheckConstraint(
            "(doc_type)::text = ANY (ARRAY[('PUBLICATION'::character varying)::text, ('BOOK'::character varying)::text, ('DATASET'::character varying)::text, ('PATENT'::character varying)::text])"
        ),
        CheckConstraint("pubmed_id >= 0"),
        CheckConstraint("year >= 0"),
    )

    doc_id = Column(Integer, primary_key=True)
    journal = Column(String(50), index=True)
    year = Column(SmallInteger, index=True)
    volume = Column(String(50), index=True)
    issue = Column(String(50), index=True)
    first_page = Column(String(50))
    last_page = Column(String(50))
    pubmed_id = Column(BigInteger, unique=True)
    doi = Column(String(100))
    chembl_id = Column(
        ForeignKey(
            "chembl_id_lookup.chembl_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        unique=True,
    )
    title = Column(String(500))
    doc_type = Column(String(50), nullable=False)
    authors = Column(String(4000))
    abstract = Column(Text)
    patent_id = Column(String(20))

    chembl = relationship("ChemblIdLookup", uselist=False)


class Domain(Base):
    __tablename__ = "domains"
    __table_args__ = (
        CheckConstraint(
            "(domain_type)::text = ANY (ARRAY[('Pfam-A'::character varying)::text, ('Pfam-B'::character varying)::text])"
        ),
    )

    domain_id = Column(Integer, primary_key=True)
    domain_type = Column(String(20), nullable=False)
    source_domain_id = Column(String(20), nullable=False)
    domain_name = Column(String(20))
    domain_description = Column(String(500))


class DrugIndication(Base):
    __tablename__ = "drug_indication"
    __table_args__ = (
        CheckConstraint(
            "(max_phase_for_ind >= 0) AND (max_phase_for_ind = ANY (ARRAY[0, 1, 2, 3, 4]))"
        ),
        CheckConstraint("drugind_id >= 0"),
        UniqueConstraint("record_id", "mesh_id", "efo_id"),
    )

    drugind_id = Column(Integer, primary_key=True)
    record_id = Column(
        ForeignKey(
            "compound_records.record_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    max_phase_for_ind = Column(SmallInteger)
    mesh_id = Column(String(7), nullable=False)
    mesh_heading = Column(String(200), nullable=False)
    efo_id = Column(String(20))
    efo_term = Column(String(200))

    molecule_dictionary = relationship("MoleculeDictionary")
    record = relationship("CompoundRecord")


class DrugMechanism(Base):
    __tablename__ = "drug_mechanism"
    __table_args__ = (
        CheckConstraint(
            "(direct_interaction = ANY (ARRAY[0, 1])) OR (direct_interaction IS NULL)"
        ),
        CheckConstraint(
            "(disease_efficacy = ANY (ARRAY[0, 1])) OR (disease_efficacy IS NULL)"
        ),
        CheckConstraint(
            "(molecular_mechanism = ANY (ARRAY[0, 1])) OR (molecular_mechanism IS NULL)"
        ),
    )

    mec_id = Column(Integer, primary_key=True)
    record_id = Column(
        ForeignKey(
            "compound_records.record_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    mechanism_of_action = Column(String(250))
    tid = Column(
        ForeignKey(
            "target_dictionary.tid", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    site_id = Column(
        ForeignKey(
            "binding_sites.site_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    action_type = Column(String(50), index=True)
    direct_interaction = Column(SmallInteger)
    molecular_mechanism = Column(SmallInteger)
    disease_efficacy = Column(SmallInteger)
    mechanism_comment = Column(String(500))
    selectivity_comment = Column(String(100))
    binding_site_comment = Column(String(100))

    molecule_dictionary = relationship("MoleculeDictionary")
    record = relationship("CompoundRecord")
    site = relationship("BindingSite")
    target_dictionary = relationship("TargetDictionary")


class Formulation(Base):
    __tablename__ = "formulations"
    __table_args__ = (UniqueConstraint("record_id", "product_id"),)

    product_id = Column(
        ForeignKey(
            "products.product_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    ingredient = Column(String(200))
    strength = Column(String(200))
    record_id = Column(
        ForeignKey(
            "compound_records.record_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    formulation_id = Column(Integer, primary_key=True)

    molecule_dictionary = relationship("MoleculeDictionary")
    product = relationship("Product")
    record = relationship("CompoundRecord")


class FracClassification(Base):
    __tablename__ = "frac_classification"

    frac_class_id = Column(Integer, primary_key=True)
    active_ingredient = Column(String(500), nullable=False)
    level1 = Column(String(2), nullable=False)
    level1_description = Column(String(2000), nullable=False)
    level2 = Column(String(2), nullable=False)
    level2_description = Column(String(2000))
    level3 = Column(String(6), nullable=False)
    level3_description = Column(String(2000))
    level4 = Column(String(7), nullable=False)
    level4_description = Column(String(2000))
    level5 = Column(String(8), nullable=False, unique=True)
    frac_code = Column(String(4), nullable=False)


class GoClassification(Base):
    __tablename__ = "go_classification"
    __table_args__ = (
        CheckConstraint(
            "(aspect)::text = ANY (ARRAY[('C'::character varying)::text, ('F'::character varying)::text, ('P'::character varying)::text])"
        ),
        CheckConstraint(
            "(class_level >= 0) AND (class_level = ANY (ARRAY[0, 1, 2, 3, 4, 5, 6, 7]))"
        ),
    )

    go_id = Column(String(10), primary_key=True, index=True)
    parent_go_id = Column(String(10))
    pref_name = Column(String(200))
    class_level = Column(SmallInteger)
    aspect = Column(String(1))
    path = Column(String(1000))


class HracClassification(Base):
    __tablename__ = "hrac_classification"

    hrac_class_id = Column(Integer, primary_key=True)
    active_ingredient = Column(String(500), nullable=False)
    level1 = Column(String(2), nullable=False)
    level1_description = Column(String(2000), nullable=False)
    level2 = Column(String(3), nullable=False)
    level2_description = Column(String(2000))
    level3 = Column(String(5), nullable=False, unique=True)
    hrac_code = Column(String(2), nullable=False)


class IndicationRef(Base):
    __tablename__ = "indication_refs"
    __table_args__ = (
        CheckConstraint(
            "(ref_type)::text = ANY (ARRAY[('ATC'::character varying)::text, ('ClinicalTrials'::character varying)::text, ('DailyMed'::character varying)::text, ('FDA'::character varying)::text])"
        ),
        CheckConstraint("drugind_id >= 0"),
        CheckConstraint("indref_id >= 0"),
    )

    indref_id = Column(Integer, primary_key=True)
    drugind_id = Column(
        ForeignKey(
            "drug_indication.drugind_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    ref_type = Column(String(50), nullable=False)
    ref_id = Column(String(2000), nullable=False)
    ref_url = Column(String(4000), nullable=False)

    drugind = relationship("DrugIndication")


class IracClassification(Base):
    __tablename__ = "irac_classification"
    __table_args__ = (
        CheckConstraint(
            "(level1)::text = ANY (ARRAY[('A'::character varying)::text, ('B'::character varying)::text, ('C'::character varying)::text, ('D'::character varying)::text, ('E'::character varying)::text, ('M'::character varying)::text, ('U'::character varying)::text])"
        ),
        CheckConstraint(
            "(level1_description)::text = ANY (ARRAY[('ENERGY METABOLISM'::character varying)::text, ('GROWTH REGULATION'::character varying)::text, ('LIPID SYNTHESIS, GROWTH REGULATION'::character varying)::text, ('MISCELLANEOUS'::character varying)::text, ('NERVE ACTION'::character varying)::text, ('NERVE AND MUSCLE ACTION'::character varying)::text, ('UNKNOWN'::character varying)::text])"
        ),
    )

    irac_class_id = Column(Integer, primary_key=True)
    active_ingredient = Column(String(500), nullable=False)
    level1 = Column(String(1), nullable=False)
    level1_description = Column(String(2000), nullable=False)
    level2 = Column(String(3), nullable=False)
    level2_description = Column(String(2000), nullable=False)
    level3 = Column(String(6), nullable=False)
    level3_description = Column(String(2000), nullable=False)
    level4 = Column(String(8), nullable=False, unique=True)
    irac_code = Column(String(3), nullable=False)


class MechanismRef(Base):
    __tablename__ = "mechanism_refs"
    __table_args__ = (
        CheckConstraint(
            "(ref_type)::text = ANY (ARRAY[('ISBN'::character varying)::text, ('IUPHAR'::character varying)::text, ('DOI'::character varying)::text, ('EMA'::character varying)::text, ('PubMed'::character varying)::text, ('USPO'::character varying)::text, ('DailyMed'::character varying)::text, ('FDA'::character varying)::text, ('Expert'::character varying)::text, ('Other'::character varying)::text, ('InterPro'::character varying)::text, ('Wikipedia'::character varying)::text, ('UniProt'::character varying)::text, ('KEGG'::character varying)::text, ('PMC'::character varying)::text, ('ClinicalTrials'::character varying)::text, ('Patent'::character varying)::text])"
        ),
        UniqueConstraint("mec_id", "ref_type", "ref_id"),
    )

    mecref_id = Column(Integer, primary_key=True)
    mec_id = Column(
        ForeignKey(
            "drug_mechanism.mec_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    ref_type = Column(String(50), nullable=False)
    ref_id = Column(String(200))
    ref_url = Column(String(400))

    mec = relationship("DrugMechanism")


class Metabolism(Base):
    __tablename__ = "metabolism"
    __table_args__ = (
        CheckConstraint(
            "(organism)::text = ANY (ARRAY[('Callithrix jacchus'::character varying)::text, ('Canis lupus familiaris'::character varying)::text, ('Homo sapiens'::character varying)::text, ('Mus musculus'::character varying)::text, ('Oryctolagus cuniculus'::character varying)::text, ('Rattus norvegicus'::character varying)::text])"
        ),
        CheckConstraint("pathway_id >= 0"),
        CheckConstraint("tax_id >= 0"),
        UniqueConstraint(
            "drug_record_id",
            "substrate_record_id",
            "metabolite_record_id",
            "pathway_id",
            "enzyme_name",
            "enzyme_tid",
            "tax_id",
        ),
    )

    met_id = Column(Integer, primary_key=True)
    drug_record_id = Column(
        ForeignKey(
            "compound_records.record_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    substrate_record_id = Column(
        ForeignKey(
            "compound_records.record_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    metabolite_record_id = Column(
        ForeignKey(
            "compound_records.record_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    pathway_id = Column(Integer)
    pathway_key = Column(String(50))
    enzyme_name = Column(String(200))
    enzyme_tid = Column(
        ForeignKey(
            "target_dictionary.tid", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    met_conversion = Column(String(200))
    organism = Column(String(100))
    tax_id = Column(BigInteger)
    met_comment = Column(String(1000))

    drug_record = relationship(
        "CompoundRecord",
        primaryjoin="Metabolism.drug_record_id == CompoundRecord.record_id",
    )
    target_dictionary = relationship("TargetDictionary")
    metabolite_record = relationship(
        "CompoundRecord",
        primaryjoin="Metabolism.metabolite_record_id == CompoundRecord.record_id",
    )
    substrate_record = relationship(
        "CompoundRecord",
        primaryjoin="Metabolism.substrate_record_id == CompoundRecord.record_id",
    )


class MetabolismRef(Base):
    __tablename__ = "metabolism_refs"
    __table_args__ = (
        CheckConstraint(
            "(ref_type)::text = ANY (ARRAY[('DAILYMED'::character varying)::text, ('DOI'::character varying)::text, ('DailyMed'::character varying)::text, ('FDA'::character varying)::text, ('ISBN'::character varying)::text, ('OTHER'::character varying)::text, ('PMID'::character varying)::text])"
        ),
        UniqueConstraint("met_id", "ref_type", "ref_id"),
    )

    metref_id = Column(Integer, primary_key=True)
    met_id = Column(
        ForeignKey("metabolism.met_id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    ref_type = Column(String(50), nullable=False)
    ref_id = Column(String(200))
    ref_url = Column(String(400))

    met = relationship("Metabolism")


class MoleculeAtcClassification(Base):
    __tablename__ = "molecule_atc_classification"

    mol_atc_id = Column(Integer, primary_key=True)
    level5 = Column(
        ForeignKey(
            "atc_classification.level5", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )

    atc_classification = relationship("AtcClassification")
    molecule_dictionary = relationship("MoleculeDictionary")


class MoleculeDictionary(Base):
    __tablename__ = "molecule_dictionary"
    __table_args__ = (
        CheckConstraint(
            "(max_phase >= 0) AND (max_phase = ANY (ARRAY[0, 1, 2, 3, 4]))"
        ),
        CheckConstraint(
            "(molecule_type)::text = ANY (ARRAY[('Antibody'::character varying)::text, ('Cell'::character varying)::text, ('Enzyme'::character varying)::text, ('Oligonucleotide'::character varying)::text, ('Oligosaccharide'::character varying)::text, ('Protein'::character varying)::text, ('Small molecule'::character varying)::text, ('Unclassified'::character varying)::text, ('Unknown'::character varying)::text])"
        ),
        CheckConstraint(
            "(polymer_flag = ANY (ARRAY[0, 1])) OR (polymer_flag IS NULL)"
        ),
        CheckConstraint(
            "(structure_type)::text = ANY (ARRAY[('NONE'::character varying)::text, ('MOL'::character varying)::text, ('SEQ'::character varying)::text, ('BOTH'::character varying)::text])"
        ),
        CheckConstraint(
            "availability_type = ANY (ARRAY['-2'::integer, '-1'::integer, 0, 1, 2])"
        ),
        CheckConstraint(
            "black_box_warning = ANY (ARRAY[0, 1, '-1'::integer])"
        ),
        CheckConstraint("chebi_par_id >= 0"),
        CheckConstraint("chirality = ANY (ARRAY['-1'::integer, 0, 1, 2])"),
        CheckConstraint("dosed_ingredient = ANY (ARRAY[0, 1])"),
        CheckConstraint("first_approval >= 0"),
        CheckConstraint("first_in_class = ANY (ARRAY[0, 1, '-1'::integer])"),
        CheckConstraint("inorganic_flag = ANY (ARRAY[0, 1, '-1'::integer])"),
        CheckConstraint("natural_product = ANY (ARRAY[0, 1, '-1'::integer])"),
        CheckConstraint("oral = ANY (ARRAY[0, 1])"),
        CheckConstraint("parenteral = ANY (ARRAY[0, 1])"),
        CheckConstraint("prodrug = ANY (ARRAY[0, 1, '-1'::integer])"),
        CheckConstraint("therapeutic_flag = ANY (ARRAY[0, 1])"),
        CheckConstraint("topical = ANY (ARRAY[0, 1])"),
        CheckConstraint("usan_year >= 0"),
        CheckConstraint("withdrawn_flag = ANY (ARRAY[0, 1])"),
        CheckConstraint("withdrawn_year >= 0"),
    )

    molregno = Column(Integer, primary_key=True)
    pref_name = Column(String(255), index=True)
    chembl_id = Column(
        ForeignKey(
            "chembl_id_lookup.chembl_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        unique=True,
    )
    max_phase = Column(
        SmallInteger, nullable=False, index=True, server_default=text("0")
    )
    therapeutic_flag = Column(
        SmallInteger, nullable=False, index=True, server_default=text("0")
    )
    dosed_ingredient = Column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    structure_type = Column(String(10), nullable=False)
    chebi_par_id = Column(Integer)
    molecule_type = Column(String(30))
    first_approval = Column(SmallInteger)
    oral = Column(SmallInteger, nullable=False, server_default=text("0"))
    parenteral = Column(SmallInteger, nullable=False, server_default=text("0"))
    topical = Column(SmallInteger, nullable=False, server_default=text("0"))
    black_box_warning = Column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    natural_product = Column(
        SmallInteger, nullable=False, server_default=text("'-1'::integer")
    )
    first_in_class = Column(
        SmallInteger, nullable=False, server_default=text("'-1'::integer")
    )
    chirality = Column(
        SmallInteger, nullable=False, server_default=text("'-1'::integer")
    )
    prodrug = Column(
        SmallInteger, nullable=False, server_default=text("'-1'::integer")
    )
    inorganic_flag = Column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    usan_year = Column(SmallInteger)
    availability_type = Column(SmallInteger)
    usan_stem = Column(String(50))
    polymer_flag = Column(SmallInteger)
    usan_substem = Column(String(50))
    usan_stem_definition = Column(String(1000))
    indication_class = Column(String(1000))
    withdrawn_flag = Column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    withdrawn_year = Column(SmallInteger)
    withdrawn_country = Column(String(2000))
    withdrawn_reason = Column(String(2000))

    chembl = relationship("ChemblIdLookup", uselist=False)


class Biotherapeutic(MoleculeDictionary):
    __tablename__ = "biotherapeutics"

    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        primary_key=True,
    )
    description = Column(String(2000))
    helm_notation = Column(String(4000))


class CompoundProperty(MoleculeDictionary):
    __tablename__ = "compound_properties"
    __table_args__ = (
        CheckConstraint(
            "(molecular_species)::text = ANY (ARRAY[('ACID'::character varying)::text, ('BASE'::character varying)::text, ('ZWITTERION'::character varying)::text, ('NEUTRAL'::character varying)::text])"
        ),
        CheckConstraint(
            "(num_lipinski_ro5_violations >= 0) AND (num_lipinski_ro5_violations = ANY (ARRAY[0, 1, 2, 3, 4]))"
        ),
        CheckConstraint(
            "(num_ro5_violations >= 0) AND (num_ro5_violations = ANY (ARRAY[0, 1, 2, 3, 4]))"
        ),
        CheckConstraint(
            "(ro3_pass)::text = ANY (ARRAY[('Y'::character varying)::text, ('N'::character varying)::text])"
        ),
        CheckConstraint("acd_most_bpka >= (0)::numeric"),
        CheckConstraint("aromatic_rings >= 0"),
        CheckConstraint("full_mwt >= (0)::numeric"),
        CheckConstraint("hba >= 0"),
        CheckConstraint("hba_lipinski >= 0"),
        CheckConstraint("hbd >= 0"),
        CheckConstraint("hbd_lipinski >= 0"),
        CheckConstraint("heavy_atoms >= 0"),
        CheckConstraint("mw_freebase >= (0)::numeric"),
        CheckConstraint("mw_monoisotopic >= (0)::numeric"),
        CheckConstraint("num_alerts >= 0"),
        CheckConstraint("psa >= (0)::numeric"),
        CheckConstraint("qed_weighted >= (0)::numeric"),
        CheckConstraint("rtb >= 0"),
    )

    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        primary_key=True,
    )
    mw_freebase = Column(Numeric(9, 2), index=True)
    alogp = Column(Numeric(9, 2), index=True)
    hba = Column(SmallInteger, index=True)
    hbd = Column(SmallInteger, index=True)
    psa = Column(Numeric(9, 2), index=True)
    rtb = Column(SmallInteger, index=True)
    ro3_pass = Column(String(3))
    num_ro5_violations = Column(SmallInteger, index=True)
    acd_most_apka = Column(Numeric(9, 2))
    acd_most_bpka = Column(Numeric(9, 2))
    acd_logp = Column(Numeric(9, 2))
    acd_logd = Column(Numeric(9, 2))
    molecular_species = Column(String(50))
    full_mwt = Column(Numeric(9, 2))
    aromatic_rings = Column(SmallInteger)
    heavy_atoms = Column(SmallInteger)
    num_alerts = Column(SmallInteger)
    qed_weighted = Column(Numeric(3, 2))
    mw_monoisotopic = Column(Numeric(11, 4))
    full_molformula = Column(String(100))
    hba_lipinski = Column(SmallInteger)
    hbd_lipinski = Column(SmallInteger)
    num_lipinski_ro5_violations = Column(SmallInteger)


class CompoundStructure(MoleculeDictionary):
    __tablename__ = "compound_structures"

    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        primary_key=True,
    )
    molfile = Column(Text)
    standard_inchi = Column(String(4000))
    standard_inchi_key = Column(String(27), nullable=False, index=True)
    canonical_smiles = Column(String(4000))


class MoleculeHierarchy(MoleculeDictionary):
    __tablename__ = "molecule_hierarchy"

    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        primary_key=True,
    )
    parent_molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    active_molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )

    molecule_dictionary = relationship(
        "MoleculeDictionary",
        primaryjoin="MoleculeHierarchy.active_molregno == MoleculeDictionary.molregno",
    )
    molecule_dictionary1 = relationship(
        "MoleculeDictionary",
        primaryjoin="MoleculeHierarchy.parent_molregno == MoleculeDictionary.molregno",
    )


class MoleculeFracClassification(Base):
    __tablename__ = "molecule_frac_classification"
    __table_args__ = (UniqueConstraint("frac_class_id", "molregno"),)

    mol_frac_id = Column(Integer, primary_key=True)
    frac_class_id = Column(
        ForeignKey(
            "frac_classification.frac_class_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )

    frac_class = relationship("FracClassification")
    molecule_dictionary = relationship("MoleculeDictionary")


class MoleculeHracClassification(Base):
    __tablename__ = "molecule_hrac_classification"
    __table_args__ = (UniqueConstraint("hrac_class_id", "molregno"),)

    mol_hrac_id = Column(Integer, primary_key=True)
    hrac_class_id = Column(
        ForeignKey(
            "hrac_classification.hrac_class_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )

    hrac_class = relationship("HracClassification")
    molecule_dictionary = relationship("MoleculeDictionary")


class MoleculeIracClassification(Base):
    __tablename__ = "molecule_irac_classification"
    __table_args__ = (UniqueConstraint("irac_class_id", "molregno"),)

    mol_irac_id = Column(Integer, primary_key=True)
    irac_class_id = Column(
        ForeignKey(
            "irac_classification.irac_class_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )

    irac_class = relationship("IracClassification")
    molecule_dictionary = relationship("MoleculeDictionary")


class MoleculeSynonym(Base):
    __tablename__ = "molecule_synonyms"
    __table_args__ = (UniqueConstraint("molregno", "synonyms", "syn_type"),)

    molregno = Column(
        ForeignKey(
            "molecule_dictionary.molregno",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    synonyms = Column(String(200), index=True)
    syn_type = Column(String(50), nullable=False)
    molsyn_id = Column(Integer, primary_key=True)
    res_stem_id = Column(
        ForeignKey(
            "research_stem.res_stem_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )

    molecule_dictionary = relationship("MoleculeDictionary")
    res_stem = relationship("ResearchStem")


class OrganismClas(Base):
    __tablename__ = "organism_class"
    __table_args__ = (CheckConstraint("tax_id >= 0"),)

    oc_id = Column(Integer, primary_key=True)
    tax_id = Column(BigInteger, unique=True)
    l1 = Column(String(200))
    l2 = Column(String(200))
    l3 = Column(String(200))


class ParameterType(Base):
    __tablename__ = "parameter_type"

    parameter_type = Column(String(40), primary_key=True, index=True)
    description = Column(String(2000))


class PatentUseCode(Base):
    __tablename__ = "patent_use_codes"

    patent_use_code = Column(String(8), primary_key=True, index=True)
    definition = Column(String(500), nullable=False)


class PredictedBindingDomain(Base):
    __tablename__ = "predicted_binding_domains"
    __table_args__ = (
        CheckConstraint(
            "(confidence)::text = ANY (ARRAY[('high'::character varying)::text, ('medium'::character varying)::text, ('low'::character varying)::text])"
        ),
        CheckConstraint(
            "(prediction_method)::text = ANY (ARRAY[('Manual'::character varying)::text, ('Multi domain'::character varying)::text, ('Single domain'::character varying)::text])"
        ),
    )

    predbind_id = Column(Integer, primary_key=True)
    activity_id = Column(
        ForeignKey(
            "activities.activity_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    site_id = Column(
        ForeignKey(
            "binding_sites.site_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    prediction_method = Column(String(50))
    confidence = Column(String(10))

    activity = relationship("Activity")
    site = relationship("BindingSite")


class ProductPatent(Base):
    __tablename__ = "product_patents"
    __table_args__ = (
        CheckConstraint("delist_flag = ANY (ARRAY[0, 1])"),
        CheckConstraint("drug_product_flag = ANY (ARRAY[0, 1])"),
        CheckConstraint("drug_substance_flag = ANY (ARRAY[0, 1])"),
        UniqueConstraint(
            "product_id", "patent_no", "patent_expire_date", "patent_use_code"
        ),
    )

    prod_pat_id = Column(Integer, primary_key=True)
    product_id = Column(
        ForeignKey(
            "products.product_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    patent_no = Column(String(11), nullable=False)
    patent_expire_date = Column(Date, nullable=False)
    drug_substance_flag = Column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    drug_product_flag = Column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    patent_use_code = Column(
        ForeignKey(
            "patent_use_codes.patent_use_code",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    delist_flag = Column(
        SmallInteger, nullable=False, server_default=text("0")
    )

    patent_use_code1 = relationship("PatentUseCode")
    product = relationship("Product")


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint(
            "(ad_type)::text = ANY (ARRAY[('OTC'::character varying)::text, ('RX'::character varying)::text, ('DISCN'::character varying)::text])"
        ),
        CheckConstraint(
            "(black_box_warning = ANY (ARRAY[0, 1])) OR (black_box_warning IS NULL)"
        ),
        CheckConstraint(
            "(innovator_company = ANY (ARRAY[0, 1])) OR (innovator_company IS NULL)"
        ),
        CheckConstraint(
            "(nda_type)::text = ANY (ARRAY[('N'::character varying)::text, ('A'::character varying)::text])"
        ),
        CheckConstraint("(oral = ANY (ARRAY[0, 1])) OR (oral IS NULL)"),
        CheckConstraint(
            "(parenteral = ANY (ARRAY[0, 1])) OR (parenteral IS NULL)"
        ),
        CheckConstraint("(topical = ANY (ARRAY[0, 1])) OR (topical IS NULL)"),
    )

    dosage_form = Column(String(200))
    route = Column(String(200))
    trade_name = Column(String(200))
    approval_date = Column(Date)
    ad_type = Column(String(5))
    oral = Column(SmallInteger)
    topical = Column(SmallInteger)
    parenteral = Column(SmallInteger)
    black_box_warning = Column(SmallInteger)
    applicant_full_name = Column(String(200))
    innovator_company = Column(SmallInteger)
    product_id = Column(String(30), primary_key=True, index=True)
    nda_type = Column(String(10))


class ProteinClassSynonym(Base):
    __tablename__ = "protein_class_synonyms"
    __table_args__ = (
        CheckConstraint(
            "(syn_type)::text = ANY (ARRAY[('CHEMBL'::character varying)::text, ('CONCEPT_WIKI'::character varying)::text, ('UMLS'::character varying)::text, ('CW_XREF'::character varying)::text, ('MESH_XREF'::character varying)::text])"
        ),
    )

    protclasssyn_id = Column(Integer, primary_key=True)
    protein_class_id = Column(
        ForeignKey(
            "protein_classification.protein_class_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    protein_class_synonym = Column(String(1000))
    syn_type = Column(String(20))

    protein_class = relationship("ProteinClassification")


class ProteinClassification(Base):
    __tablename__ = "protein_classification"
    __table_args__ = (
        CheckConstraint(
            "(class_level >= 0) AND (class_level = ANY (ARRAY[0, 1, 2, 3, 4, 5, 6, 7, 8]))"
        ),
        CheckConstraint("parent_id >= 0"),
    )

    protein_class_id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    pref_name = Column(String(500))
    short_name = Column(String(50))
    protein_class_desc = Column(String(410), nullable=False)
    definition = Column(String(4000))
    class_level = Column(Integer, nullable=False)


class ProteinFamilyClassification(Base):
    __tablename__ = "protein_family_classification"
    __table_args__ = (
        UniqueConstraint("l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8"),
    )

    protein_class_id = Column(Integer, primary_key=True)
    protein_class_desc = Column(String(810), nullable=False, unique=True)
    l1 = Column(String(100), nullable=False)
    l2 = Column(String(100))
    l3 = Column(String(100))
    l4 = Column(String(100))
    l5 = Column(String(100))
    l6 = Column(String(100))
    l7 = Column(String(100))
    l8 = Column(String(100))


class RelationshipType(Base):
    __tablename__ = "relationship_type"

    relationship_type = Column(String(1), primary_key=True, index=True)
    relationship_desc = Column(String(250))


class ResearchCompany(Base):
    __tablename__ = "research_companies"
    __table_args__ = (UniqueConstraint("res_stem_id", "company"),)

    co_stem_id = Column(Integer, primary_key=True)
    res_stem_id = Column(
        ForeignKey(
            "research_stem.res_stem_id", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    company = Column(String(100))
    country = Column(String(50))
    previous_company = Column(String(100))

    res_stem = relationship("ResearchStem")


class ResearchStem(Base):
    __tablename__ = "research_stem"

    res_stem_id = Column(Integer, primary_key=True)
    research_stem = Column(String(20), unique=True)


class SiteComponent(Base):
    __tablename__ = "site_components"
    __table_args__ = (
        UniqueConstraint("site_id", "component_id", "domain_id"),
    )

    sitecomp_id = Column(Integer, primary_key=True)
    site_id = Column(
        ForeignKey(
            "binding_sites.site_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    component_id = Column(
        ForeignKey(
            "component_sequences.component_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        index=True,
    )
    domain_id = Column(
        ForeignKey("domains.domain_id", deferrable=True, initially="DEFERRED"),
        index=True,
    )
    site_residues = Column(String(2000))

    component = relationship("ComponentSequence")
    domain = relationship("Domain")
    site = relationship("BindingSite")


class Source(Base):
    __tablename__ = "source"

    src_id = Column(SmallInteger, primary_key=True)
    src_description = Column(String(500))
    src_short_name = Column(String(20))


class StructuralAlertSet(Base):
    __tablename__ = "structural_alert_sets"
    __table_args__ = (
        CheckConstraint("alert_set_id >= 0"),
        CheckConstraint("priority >= 0"),
    )

    alert_set_id = Column(Integer, primary_key=True)
    set_name = Column(String(100), nullable=False, unique=True)
    priority = Column(SmallInteger, nullable=False)


class StructuralAlert(Base):
    __tablename__ = "structural_alerts"
    __table_args__ = (
        CheckConstraint("alert_id >= 0"),
        CheckConstraint("alert_set_id >= 0"),
    )

    alert_id = Column(Integer, primary_key=True)
    alert_set_id = Column(
        ForeignKey(
            "structural_alert_sets.alert_set_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    alert_name = Column(String(100), nullable=False)
    smarts = Column(String(4000), nullable=False)

    alert_set = relationship("StructuralAlertSet")


class TargetComponent(Base):
    __tablename__ = "target_components"
    __table_args__ = (
        CheckConstraint(
            "(homologue >= 0) AND (homologue = ANY (ARRAY[0, 1, 2]))"
        ),
    )

    tid = Column(
        ForeignKey(
            "target_dictionary.tid", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    component_id = Column(
        ForeignKey(
            "component_sequences.component_id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
        index=True,
    )
    targcomp_id = Column(Integer, primary_key=True)
    homologue = Column(SmallInteger, nullable=False, server_default=text("0"))

    component = relationship("ComponentSequence")
    target_dictionary = relationship("TargetDictionary")


class TargetDictionary(Base):
    __tablename__ = "target_dictionary"
    __table_args__ = (
        CheckConstraint("species_group_flag = ANY (ARRAY[0, 1])"),
        CheckConstraint("tax_id >= 0"),
    )

    tid = Column(Integer, primary_key=True)
    target_type = Column(
        ForeignKey(
            "target_type.target_type", deferrable=True, initially="DEFERRED"
        ),
        index=True,
    )
    pref_name = Column(String(200), nullable=False, index=True)
    tax_id = Column(BigInteger, index=True)
    organism = Column(String(150), index=True)
    chembl_id = Column(
        ForeignKey(
            "chembl_id_lookup.chembl_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    species_group_flag = Column(
        SmallInteger, nullable=False, server_default=text("0")
    )

    chembl = relationship("ChemblIdLookup")
    target_type1 = relationship("TargetType")


class TargetRelation(Base):
    __tablename__ = "target_relations"
    __table_args__ = (
        CheckConstraint(
            "(relationship)::text = ANY (ARRAY[('EQUIVALENT TO'::character varying)::text, ('OVERLAPS WITH'::character varying)::text, ('SUBSET OF'::character varying)::text, ('SUPERSET OF'::character varying)::text])"
        ),
    )

    tid = Column(
        ForeignKey(
            "target_dictionary.tid", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    relationship = Column(String(20), nullable=False)
    related_tid = Column(
        ForeignKey(
            "target_dictionary.tid", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        index=True,
    )
    targrel_id = Column(Integer, primary_key=True)

    target_dictionary = relationship(
        "TargetDictionary",
        primaryjoin="TargetRelation.related_tid == TargetDictionary.tid",
    )
    target_dictionary1 = relationship(
        "TargetDictionary",
        primaryjoin="TargetRelation.tid == TargetDictionary.tid",
    )


class TargetType(Base):
    __tablename__ = "target_type"

    target_type = Column(String(30), primary_key=True, index=True)
    target_desc = Column(String(250))
    parent_type = Column(String(25))


class TissueDictionary(Base):
    __tablename__ = "tissue_dictionary"
    __table_args__ = (UniqueConstraint("uberon_id", "efo_id"),)

    tissue_id = Column(Integer, primary_key=True)
    uberon_id = Column(String(15))
    pref_name = Column(String(200), nullable=False)
    efo_id = Column(String(20))
    chembl_id = Column(
        ForeignKey(
            "chembl_id_lookup.chembl_id", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
        unique=True,
    )
    bto_id = Column(String(20))
    caloha_id = Column(String(7))

    chembl = relationship("ChemblIdLookup", uselist=False)


class UsanStem(Base):
    __tablename__ = "usan_stems"
    __table_args__ = (
        CheckConstraint(
            "(major_class)::text = ANY (ARRAY[('GPCR'::character varying)::text, ('NR'::character varying)::text, ('PDE'::character varying)::text, ('ion channel'::character varying)::text, ('kinase'::character varying)::text, ('protease'::character varying)::text])"
        ),
        CheckConstraint(
            "(stem_class)::text = ANY (ARRAY[('Suffix'::character varying)::text, ('Prefix'::character varying)::text, ('Infix'::character varying)::text])"
        ),
        CheckConstraint(
            "(who_extra = ANY (ARRAY[0, 1])) OR (who_extra IS NULL)"
        ),
        CheckConstraint("usan_stem_id >= 0"),
        UniqueConstraint("stem", "subgroup"),
    )

    usan_stem_id = Column(Integer, primary_key=True)
    stem = Column(String(100), nullable=False)
    subgroup = Column(String(100), nullable=False)
    annotation = Column(String(2000))
    stem_class = Column(String(100))
    major_class = Column(String(100))
    who_extra = Column(SmallInteger, server_default=text("0"))


class VariantSequence(Base):
    __tablename__ = "variant_sequences"
    __table_args__ = (
        CheckConstraint("(isoform >= 0) AND (isoform = ANY (ARRAY[1, 2, 4]))"),
        CheckConstraint(
            "(version >= 0) AND (version = ANY (ARRAY[1, 2, 3, 4, 5]))"
        ),
        CheckConstraint("variant_id >= 0"),
    )

    variant_id = Column(Integer, primary_key=True)
    mutation = Column(String(2000))
    accession = Column(String(25))
    version = Column(Integer)
    isoform = Column(Integer)
    sequence = Column(Text)
    organism = Column(String(200))


class Version(Base):
    __tablename__ = "version"

    name = Column(String(20), primary_key=True, index=True)
    creation_date = Column(Date)
    comments = Column(String(2000))
