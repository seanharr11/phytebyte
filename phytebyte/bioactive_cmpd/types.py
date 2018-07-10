from collections import namedtuple


BioactiveCompound = namedtuple("BioactiveCompound", [
    "uid",
    "pref_name",
    "canonical_smiles",
    "gene_target",
    "name",
    "bioactivities"])

# Used in ChemblBioactiveCompoundQuery to filter BioactivityAssays
BioactivityStandardFilter = namedtuple("BioactivityStandardFilter", [
    "types",
    "relations",
    "units",
    "max_value"])

BioactiveCompoundMechanism = namedtuple("BioactiveCompoundMechanism", [
    "mechanism_of_action", "action_type", "comment"])

CompoundBioactivity = namedtuple("CompoundBioactivity", [
    "amount", "units", "type", "descr"])
