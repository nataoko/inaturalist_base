from pyinaturalist import *

obs = get_observations(user_id='niconoe', per_page=5) # dictionary of observations
print(type(obs))
for i in obs.keys():
    print(i)
print(list(obs.keys())[0])
total_results, page, per_page, results = list(obs.values())
print(total_results, page, per_page, len(results))
#print(results[0])
pprint(results)


#from pyinaturalist import Observation, get_observations
response = get_observations(user_id='niconoe')
observations = Observation.from_json_list(response)

#from pyinaturalist import get_access_token
access_token = get_access_token(
    username='nataoko',  # Username you use to login to iNaturalist.org
    password='inat_haslo',  # Password you use to login to iNaturalist.org
    app_id='_3enzD21jxrFkRTum5POJeYl8VCG7BZ9g2R9lmCkD4o',  # OAuth2 application ID
    app_secret='g351BmZkYa9Dc4-zh0PdEQ0lVxifw2RWLpdtvX061ko',  # OAuth2 application secret
)
import os
os.environ['INAT_USERNAME'] = 'nataoko'
os.environ['INAT_PASSWORD'] = 'inat_haslo'
os.environ['INAT_APP_ID'] = '_3enzD21jxrFkRTum5POJeYl8VCG7BZ9g2R9lmCkD4o'
os.environ['INAT_APP_SECRET'] = 'g351BmZkYa9Dc4-zh0PdEQ0lVxifw2RWLpdtvX061ko'
