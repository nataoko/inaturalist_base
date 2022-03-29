import json
import os
import shutil


def generate_new_data_file():
    data = {"areas": {}, "observations": []}
    with open('data'+os.sep+'data.json', 'w') as outfile:
        outfile.write(json.dumps(data))


def open_data():
    shutil.copyfile('data'+os.sep+'data.json', 'data'+os.sep+'data_bk.json')
    return json.load(open('data'+os.sep+'data.json'))


def save_new_area(name, locs, data):
    data['areas'][name] = locs
    with open('data'+os.sep+'data.json', 'w') as outfile:
        outfile.write(json.dumps(data))
    return data

