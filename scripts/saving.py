import json
import os
import shutil



def open_data():
    shutil.copyfile('data'+os.sep+'data.json', 'data'+os.sep+'data_bk.json')
    return json.load(open('data'+os.sep+'data.json'))


def valid_name(name, data):
    if not name.isalnum():
        return 1
    if name in data['areas']:
        return 2
    return name


def save_new_area(name, locs, data):
    data['areas'][name] = locs
    with open('data'+os.sep+'data.json', 'w') as outfile:
        outfile.write(json.dumps(data))
    return data

