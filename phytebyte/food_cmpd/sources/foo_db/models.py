# coding: utf-8
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class CompoundAlternateParent(Base):
    __tablename__ = "compound_alternate_parents"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    compound_id = Column(ForeignKey("compounds.id"), index=True)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    compound = relationship("Compound")


class CompoundExternalDescriptor(Base):
    __tablename__ = "compound_external_descriptors"

    id = Column(Integer, primary_key=True)
    external_id = Column(String(255))
    annotations = Column(String(255))
    compound_id = Column(ForeignKey("compounds.id"), index=True)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    compound = relationship("Compound")


class CompoundSubstituent(Base):
    __tablename__ = "compound_substituents"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    compound_id = Column(ForeignKey("compounds.id"), index=True)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    compound = relationship("Compound")


class CompoundSynonym(Base):
    __tablename__ = "compound_synonyms"
    __table_args__ = (
        Index(
            "index_compound_synonyms_on_source_id_and_source_type",
            "source_id",
            "source_type",
        ),
    )

    id = Column(Integer, primary_key=True)
    synonym = Column(String(255, "utf8_unicode_ci"), nullable=False, unique=True)
    synonym_source = Column(String(255, "utf8_unicode_ci"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    source_id = Column(Integer)
    source_type = Column(String(255, "utf8_unicode_ci"))


class Compound(Base):
    __tablename__ = "compounds"
    __table_args__ = (
        Index(
            "index_compounds_on_name_and_public_id", "name", "public_id", unique=True
        ),
    )

    id = Column(Integer, primary_key=True)
    legacy_id = Column(Integer)
    type = Column(String(255, "utf8_unicode_ci"), nullable=False)
    public_id = Column(String(9, "utf8_unicode_ci"), nullable=False, unique=True)
    name = Column(String(255, "utf8_unicode_ci"), nullable=False, unique=True)
    export = Column(Integer, server_default=text("'0'"))
    state = Column(String(255, "utf8_unicode_ci"))
    annotation_quality = Column(String(255, "utf8_unicode_ci"))
    description = Column(String(collation="utf8_unicode_ci"))
    cas_number = Column(String(255, "utf8_unicode_ci"))
    melting_point = Column(String(collation="utf8_unicode_ci"))
    protein_formula = Column(String(255, "utf8_unicode_ci"))
    protein_weight = Column(String(255, "utf8_unicode_ci"))
    experimental_solubility = Column(String(255, "utf8_unicode_ci"))
    experimental_logp = Column(String(255, "utf8_unicode_ci"))
    hydrophobicity = Column(String(255, "utf8_unicode_ci"))
    isoelectric_point = Column(String(255, "utf8_unicode_ci"))
    metabolism = Column(String(collation="utf8_unicode_ci"))
    kegg_compound_id = Column(String(255, "utf8_unicode_ci"))
    pubchem_compound_id = Column(String(255, "utf8_unicode_ci"))
    pubchem_substance_id = Column(String(255, "utf8_unicode_ci"))
    chebi_id = Column(String(255, "utf8_unicode_ci"))
    het_id = Column(String(255, "utf8_unicode_ci"))
    uniprot_id = Column(String(255, "utf8_unicode_ci"))
    uniprot_name = Column(String(255, "utf8_unicode_ci"))
    genbank_id = Column(String(255, "utf8_unicode_ci"))
    wikipedia_id = Column(String(255, "utf8_unicode_ci"))
    synthesis_citations = Column(String(collation="utf8_unicode_ci"))
    general_citations = Column(String(collation="utf8_unicode_ci"))
    comments = Column(String(collation="utf8_unicode_ci"))
    protein_structure_file_name = Column(String(255, "utf8_unicode_ci"))
    protein_structure_content_type = Column(String(255, "utf8_unicode_ci"))
    protein_structure_file_size = Column(Integer)
    protein_structure_updated_at = Column(DateTime)
    msds_file_name = Column(String(255, "utf8_unicode_ci"))
    msds_content_type = Column(String(255, "utf8_unicode_ci"))
    msds_file_size = Column(Integer)
    msds_updated_at = Column(DateTime)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    phenolexplorer_id = Column(Integer)
    dfc_id = Column(String(255, "utf8_unicode_ci"))
    hmdb_id = Column(String(255, "utf8_unicode_ci"))
    duke_id = Column(String(255, "utf8_unicode_ci"))
    drugbank_id = Column(String(255, "utf8_unicode_ci"))
    bigg_id = Column(Integer)
    eafus_id = Column(String(255, "utf8_unicode_ci"))
    knapsack_id = Column(String(255, "utf8_unicode_ci"))
    boiling_point = Column(String(255, "utf8_unicode_ci"))
    boiling_point_reference = Column(String(255, "utf8_unicode_ci"))
    charge = Column(String(255, "utf8_unicode_ci"))
    charge_reference = Column(String(255, "utf8_unicode_ci"))
    density = Column(String(255, "utf8_unicode_ci"))
    density_reference = Column(String(255, "utf8_unicode_ci"))
    optical_rotation = Column(String(255, "utf8_unicode_ci"))
    optical_rotation_reference = Column(String(255, "utf8_unicode_ci"))
    percent_composition = Column(String(255, "utf8_unicode_ci"))
    percent_composition_reference = Column(String(255, "utf8_unicode_ci"))
    physical_description = Column(String(collation="utf8_unicode_ci"))
    physical_description_reference = Column(String(collation="utf8_unicode_ci"))
    refractive_index = Column(String(255, "utf8_unicode_ci"))
    refractive_index_reference = Column(String(255, "utf8_unicode_ci"))
    uv_index = Column(String(255, "utf8_unicode_ci"))
    uv_index_reference = Column(String(255, "utf8_unicode_ci"))
    experimental_pka = Column(String(255, "utf8_unicode_ci"))
    experimental_pka_reference = Column(String(255, "utf8_unicode_ci"))
    experimental_solubility_reference = Column(String(255, "utf8_unicode_ci"))
    experimental_logp_reference = Column(String(255, "utf8_unicode_ci"))
    hydrophobicity_reference = Column(String(255, "utf8_unicode_ci"))
    isoelectric_point_reference = Column(String(255, "utf8_unicode_ci"))
    melting_point_reference = Column(String(255, "utf8_unicode_ci"))
    moldb_alogps_logp = Column(String(255, "utf8_unicode_ci"))
    moldb_logp = Column(String(255, "utf8_unicode_ci"))
    moldb_alogps_logs = Column(String(255, "utf8_unicode_ci"))
    moldb_smiles = Column(String(collation="utf8_unicode_ci"))
    moldb_pka = Column(String(255, "utf8_unicode_ci"))
    moldb_formula = Column(String(255, "utf8_unicode_ci"))
    moldb_average_mass = Column(String(255, "utf8_unicode_ci"))
    moldb_inchi = Column(String(collation="utf8_unicode_ci"))
    moldb_mono_mass = Column(String(255, "utf8_unicode_ci"))
    moldb_inchikey = Column(String(255, "utf8_unicode_ci"))
    moldb_alogps_solubility = Column(String(255, "utf8_unicode_ci"))
    moldb_id = Column(Integer)
    moldb_iupac = Column(String(collation="utf8_unicode_ci"))
    structure_source = Column(String(255, "utf8_unicode_ci"))
    duplicate_id = Column(String(255, "utf8_unicode_ci"))
    old_dfc_id = Column(String(255, "utf8_unicode_ci"))
    dfc_name = Column(String(collation="utf8_unicode_ci"))
    compound_source = Column(String(255, "utf8_unicode_ci"))
    flavornet_id = Column(String(255, "utf8_unicode_ci"))
    goodscent_id = Column(String(255, "utf8_unicode_ci"))
    superscent_id = Column(String(255, "utf8_unicode_ci"))
    phenolexplorer_metabolite_id = Column(Integer)
    kingdom = Column(String(255, "utf8_unicode_ci"))
    superklass = Column(String(255, "utf8_unicode_ci"))
    klass = Column(String(255, "utf8_unicode_ci"))
    subklass = Column(String(255, "utf8_unicode_ci"))
    direct_parent = Column(String(255, "utf8_unicode_ci"))
    molecular_framework = Column(String(255, "utf8_unicode_ci"))
    chembl_id = Column(String(255, "utf8_unicode_ci"))
    chemspider_id = Column(String(255, "utf8_unicode_ci"))
    meta_cyc_id = Column(String(255, "utf8_unicode_ci"))
    foodcomex = Column(Integer)
    phytohub_id = Column(String(255, "utf8_unicode_ci"))


class CompoundsEnzyme(Base):
    __tablename__ = "compounds_enzymes"
    __table_args__ = (
        Index(
            "index_compounds_enzymes_on_compound_id_and_enzyme_id",
            "compound_id",
            "enzyme_id",
            unique=True,
        ),
    )

    id = Column(Integer, primary_key=True)
    compound_id = Column(Integer, nullable=False)
    enzyme_id = Column(Integer, nullable=False)
    citations = Column(String(collation="utf8_unicode_ci"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    creator_id = Column(Integer)
    updater_id = Column(Integer)


class CompoundsFlavor(Base):
    __tablename__ = "compounds_flavors"
    __table_args__ = (
        Index(
            "index_compounds_flavors_on_compound_id_and_flavor_id",
            "compound_id",
            "flavor_id",
            unique=True,
        ),
        Index(
            "index_compounds_flavors_on_source_id_and_source_type",
            "source_id",
            "source_type",
        ),
    )

    id = Column(Integer, primary_key=True)
    compound_id = Column(Integer, nullable=False)
    flavor_id = Column(Integer, nullable=False)
    citations = Column(String(collation="utf8_unicode_ci"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    source_id = Column(Integer)
    source_type = Column(String(255, "utf8_unicode_ci"))


class CompoundsHealthEffect(Base):
    __tablename__ = "compounds_health_effects"
    __table_args__ = (
        Index(
            "index_compounds_health_effects_on_source_id_and_source_type",
            "source_id",
            "source_type",
        ),
    )

    id = Column(Integer, primary_key=True)
    compound_id = Column(Integer, nullable=False)
    health_effect_id = Column(Integer, nullable=False)
    orig_health_effect_name = Column(String(255, "utf8_unicode_ci"))
    orig_compound_name = Column(String(255, "utf8_unicode_ci"))
    orig_citation = Column(String(collation="utf8_unicode_ci"))
    citation = Column(String(collation="utf8_unicode_ci"), nullable=False)
    citation_type = Column(String(255, "utf8_unicode_ci"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    source_id = Column(Integer)
    source_type = Column(String(255, "utf8_unicode_ci"))


class CompoundsPathway(Base):
    __tablename__ = "compounds_pathways"

    id = Column(Integer, primary_key=True)
    compound_id = Column(ForeignKey("compounds.id"), index=True)
    pathway_id = Column(ForeignKey("pathways.id"), index=True)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    compound = relationship("Compound")
    pathway = relationship("Pathway")


class Content(Base):
    __tablename__ = "contents"
    __table_args__ = (
        Index("content_source_and_food_index", "source_id", "source_type", "food_id"),
    )

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer)
    source_type = Column(String(255))
    food_id = Column(Integer, nullable=False)
    orig_food_id = Column(String(255))
    orig_food_common_name = Column(String(255))
    orig_food_scientific_name = Column(String(255))
    orig_food_part = Column(String(255))
    orig_source_id = Column(String(255))
    orig_source_name = Column(String(255))
    orig_content = Column(Numeric(15, 9))
    orig_min = Column(Numeric(15, 9))
    orig_max = Column(Numeric(15, 9))
    orig_unit = Column(String(255))
    orig_citation = Column(String)
    citation = Column(String, nullable=False)
    citation_type = Column(String(255), nullable=False)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    orig_method = Column(String(255))
    orig_unit_expression = Column(String(255))
    standard_content = Column(Numeric(15, 9))


class Enzyme(Base):
    __tablename__ = "enzymes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255, "utf8_unicode_ci"), nullable=False, unique=True)
    gene_name = Column(String(255, "utf8_unicode_ci"), unique=True)
    description = Column(String(collation="utf8_unicode_ci"))
    go_classification = Column(String(collation="utf8_unicode_ci"))
    general_function = Column(String(collation="utf8_unicode_ci"))
    specific_function = Column(String(collation="utf8_unicode_ci"))
    pathway = Column(String(collation="utf8_unicode_ci"))
    reaction = Column(String(collation="utf8_unicode_ci"))
    cellular_location = Column(String(255, "utf8_unicode_ci"))
    signals = Column(String(collation="utf8_unicode_ci"))
    transmembrane_regions = Column(String(collation="utf8_unicode_ci"))
    molecular_weight = Column(Numeric(15, 9))
    theoretical_pi = Column(Numeric(15, 9))
    locus = Column(String(255, "utf8_unicode_ci"))
    chromosome = Column(String(255, "utf8_unicode_ci"))
    uniprot_name = Column(String(255, "utf8_unicode_ci"), unique=True)
    uniprot_id = Column(String(100, "utf8_unicode_ci"), unique=True)
    pdb_id = Column(String(10, "utf8_unicode_ci"), unique=True)
    genbank_protein_id = Column(String(20, "utf8_unicode_ci"), unique=True)
    genbank_gene_id = Column(String(20, "utf8_unicode_ci"), unique=True)
    genecard_id = Column(String(20, "utf8_unicode_ci"), unique=True)
    genatlas_id = Column(String(20, "utf8_unicode_ci"), unique=True)
    hgnc_id = Column(String(20, "utf8_unicode_ci"), unique=True)
    hprd_id = Column(String(255, "utf8_unicode_ci"), unique=True)
    organism = Column(String(255, "utf8_unicode_ci"))
    general_citations = Column(String(collation="utf8_unicode_ci"))
    comments = Column(String(collation="utf8_unicode_ci"))
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Flavor(Base):
    __tablename__ = "flavors"

    id = Column(Integer, primary_key=True)
    name = Column(String(255, "utf8_unicode_ci"), nullable=False, unique=True)
    flavor_group = Column(String(255, "utf8_unicode_ci"))
    category = Column(String(255, "utf8_unicode_ci"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    creator_id = Column(Integer)
    updater_id = Column(Integer)


class FoodTaxonomy(Base):
    __tablename__ = "food_taxonomies"

    id = Column(Integer, primary_key=True)
    food_id = Column(Integer)
    ncbi_taxonomy_id = Column(Integer)
    classification_name = Column(String(255))
    classification_order = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class FoodcomexCompoundProvider(Base):
    __tablename__ = "foodcomex_compound_providers"

    id = Column(Integer, primary_key=True)
    foodcomex_compound_id = Column(Integer, nullable=False, index=True)
    provider_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class FoodcomexCompound(Base):
    __tablename__ = "foodcomex_compounds"

    id = Column(Integer, primary_key=True)
    compound_id = Column(Integer, nullable=False, index=True)
    origin = Column(String(255))
    storage_form = Column(String(255))
    maximum_quantity = Column(String(255))
    storage_condition = Column(String(255))
    contact_name = Column(String(255))
    contact_address = Column(Text)
    contact_email = Column(String(255))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    export = Column(Integer)
    purity = Column(Text)
    description = Column(Text)
    spectra_details = Column(String(255))
    delivery_time = Column(String(255))
    stability = Column(String(255))
    admin_user_id = Column(Integer, index=True)
    public_id = Column(String(255), nullable=False)
    cas_number = Column(String(255), server_default=text("''"))
    taxonomy_class = Column(String(255), server_default=text("''"))
    taxonomy_family = Column(String(255), server_default=text("''"))
    experimental_logp = Column(String(255), server_default=text("''"))
    experimental_solubility = Column(String(255), server_default=text("''"))
    melting_point = Column(String(255), server_default=text("''"))
    food_of_origin = Column(String(255), server_default=text("''"))
    production_method_reference_text = Column(Text)
    production_method_reference_file_name = Column(String(255))
    production_method_reference_content_type = Column(String(255))
    production_method_reference_file_size = Column(Integer)
    production_method_reference_updated_at = Column(DateTime)
    elemental_formula = Column(String(255), server_default=text("''"))
    minimum_quantity = Column(String(255), server_default=text("''"))
    quantity_units = Column(String(255), server_default=text("''"))
    available_spectra = Column(Text)
    storage_conditions = Column(Text)


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True)
    name = Column(String(255, "utf8_unicode_ci"), nullable=False, unique=True)
    name_scientific = Column(String(255, "utf8_unicode_ci"), index=True)
    description = Column(String(collation="utf8_unicode_ci"))
    itis_id = Column(String(255, "utf8_unicode_ci"))
    wikipedia_id = Column(String(255, "utf8_unicode_ci"))
    picture_file_name = Column(String(255, "utf8_unicode_ci"))
    picture_content_type = Column(String(255, "utf8_unicode_ci"))
    picture_file_size = Column(Integer)
    picture_updated_at = Column(DateTime)
    legacy_id = Column(Integer)
    food_group = Column(String(255, "utf8_unicode_ci"))
    food_subgroup = Column(String(255, "utf8_unicode_ci"))
    food_type = Column(String(255, "utf8_unicode_ci"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    export_to_afcdb = Column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    category = Column(String(255, "utf8_unicode_ci"))
    ncbi_taxonomy_id = Column(Integer)
    export_to_foodb = Column(Integer, server_default=text("'1'"))


class HealthEffect(Base):
    __tablename__ = "health_effects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255, "utf8_unicode_ci"), nullable=False, unique=True)
    description = Column(String(collation="utf8_unicode_ci"))
    chebi_name = Column(String(255, "utf8_unicode_ci"), index=True)
    chebi_id = Column(String(255, "utf8_unicode_ci"), index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    chebi_definition = Column(Text(collation="utf8_unicode_ci"))


class Nutrient(Base):
    __tablename__ = "nutrients"
    __table_args__ = (
        Index(
            "index_nutrients_on_name_and_public_id", "name", "public_id", unique=True
        ),
    )

    id = Column(Integer, primary_key=True)
    legacy_id = Column(Integer)
    type = Column(String(255), nullable=False)
    public_id = Column(String(9), nullable=False, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    export = Column(Integer, server_default=text("'0'"))
    state = Column(String(255))
    annotation_quality = Column(String(255))
    description = Column(String)
    wikipedia_id = Column(String(255))
    comments = Column(String)
    dfc_id = Column(String(255))
    duke_id = Column(String(255))
    eafus_id = Column(String(255))
    dfc_name = Column(String)
    compound_source = Column(String(255))
    metabolism = Column(String)
    synthesis_citations = Column(String)
    general_citations = Column(String)
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Pathway(Base):
    __tablename__ = "pathways"

    id = Column(Integer, primary_key=True)
    smpdb_id = Column(String(255, "utf8_unicode_ci"))
    kegg_map_id = Column(String(255, "utf8_unicode_ci"))
    name = Column(String(255, "utf8_unicode_ci"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Reference(Base):
    __tablename__ = "references"
    __table_args__ = (
        Index(
            "index_references_on_source_type_and_source_id", "source_type", "source_id"
        ),
    )

    id = Column(Integer, primary_key=True)
    ref_type = Column(String(255))
    text = Column(Text)
    pubmed_id = Column(String(255))
    link = Column(String(255))
    title = Column(String(255))
    creator_id = Column(Integer)
    updater_id = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    source_id = Column(Integer)
    source_type = Column(String(255))
