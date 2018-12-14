import json
import os

JSON_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

print("Merging data in {}".format(JSON_PATH))


def json_or_empty(infile):
    try:
        return json.load(infile)
    except ValueError:
        return []

def load_file(filename):
    with open(os.path.join(JSON_PATH, filename)) as infile:
        result = json_or_empty(infile)
        if len(result) == 0:
            print('Got an empty list for ', filename)
        return result

hu = load_file('hu.json')
fu = load_file('fu.json')
htw = load_file('htw.json')
beuth = load_file('beuth.json')
tu = load_file('tu.json')

with open(os.path.join(JSON_PATH, 'alle.json'), 'w') as outfile:
    outfile.write(json.dumps(hu[1:] + fu[1:] + beuth[1:] + htw[1:] + tu))

