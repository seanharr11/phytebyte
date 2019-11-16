from collections import namedtuple


BioactiveCompound = namedtuple("BioactiveCompound", [
    "uid",
    "pref_name",
    "smiles",
    "gene_target",
    "name",
    "bioactivities"])

BioactiveCompoundMechanism = namedtuple("BioactiveCompoundMechanism", [
    "mechanism_of_action", "action_type", "comment"])

CompoundBioactivity = namedtuple("CompoundBioactivity", [
    "amount", "units", "type", "descr"])
