from collections import namedtuple

# Used in ChemblBioactiveCompoundQuery to filter BioactivityAssays
BioactivityStandardFilter = namedtuple("BioactivityStandardFilter", [
    "types",
    "relations",
    "units",
    "max_value"])


agonist_bioact_filter = BioactivityStandardFilter(
    types=['EC50'], #, 'EC50'],
    # GI50 used for cytostatic investigation, cell assays (as opposed to targets),
    # IC50 is "inhibition concentration"
    # EC50 is "effective concentration" that "complements a system"
    # AC50 is "enzymatic activation"
    relations=['=', '<', '<<', '>', '>>'],
    units=['nM'],
    max_value=20000)

antagonist_bioact_filter = BioactivityStandardFilter(
    types=['IC50'], #, 'EC50'],
    # GI50 used for cytostatic investigation, cell assays (as opposed to targets),
    # IC50 is "inhibition concentration"
    # EC50 is "effective concentration" that "complements a system"
    # AC50 is "enzymatic activation"
    relations=['=', '<', '<<', '>', '>>'],
    units=['nM'],
    max_value=20000)
