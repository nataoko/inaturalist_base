from pyinaturalist import (
    Taxon,
    enable_logging,
    get_taxa,
    #get_taxa_autocomplete,
    #get_taxa_by_id,
    pprint,
)
#from rich import print


def name_list(txt):
    enable_logging()
    response = get_taxa(q=txt)#, rank=['genus', 'family'])
    taxa = Taxon.from_json_list(response)
    return taxa
