import geopandas as gpd

from pyinaturalist import (
    Taxon,
    enable_logging,
    get_taxa,
v1,
    #get_taxa_autocomplete,
    #get_taxa_by_id,
    pprint,
)
#from rich import print


def name_list(txt):
    enable_logging()
    response = get_taxa(q=txt)#, rank=['genus', 'family']) # set rank --- kingdom doesn't work
    taxa = Taxon.from_json_list(response)
    return taxa


def taxon_list(txt):
    enable_logging()
    response = get_taxa(taxon_id=txt)#, rank=['genus', 'family'])
    taxa = Taxon.from_json_list(response)
    return taxa


def gen_obs_name(txt, d1, d2, threatened):
    obs = v1.observations.get_observations(q=txt, d1=d1, d2=d2, threatened=threatened)
    pprint(obs)
    return obs#v1.observations.get_observations(q=txt)#, d1=d1, d2=d2)


def gen_obs_taxon(txt, d1, d2, threatened):
    obs = v1.observations.get_observations(taxon_id=txt, d1=d1, d2=d2, threatened=threatened)
    pprint(obs)
    return obs


def gen_countries():
    world_gdf = gpd.read_file(
        gpd.datasets.get_path('naturalearth_lowres')
    )
    countries = {
        '|'.join([j for j in world_gdf.loc[i, ['continent', 'name']]][::-1]): world_gdf.loc[i, 'geometry'] for i
        in range(len(world_gdf))}
    return countries
