import json


def load_json(file):

    # Opening JSON file
    f = open(file, )

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    return data