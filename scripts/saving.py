import json
import os
import shutil


def generate_new_data_file():
    data = {"areas": {}, "observations": []}
    with open('data'+os.sep+'data.json', 'w') as outfile:
        outfile.write(json.dumps(data))


def gen_if_error():
    shutil.copyfile('data' + os.sep + 'data_bk.json', 'data' + os.sep + 'data.json')
    return json.load(open('data' + os.sep + 'data_bk.json'))


def open_data():
    file = json.load(open('data'+os.sep+'data.json'))
    shutil.copyfile('data'+os.sep+'data.json', 'data'+os.sep+'data_bk.json')
    return file


def save_new_area(name, locs, data):
    data['areas'][name] = locs
    with open('data'+os.sep+'data.json', 'w') as outfile:
        outfile.write(json.dumps(data))
    return data

