import json
import os

def open_data:
    return json.load(open('data'+os.sep+'data.json'))

def valid_name(name, data):
    if not name.isalnum():
        return 1
    if name in data['areas']:
        return 2
    return 0

v = valid_name('2', open_data())
print(v)
