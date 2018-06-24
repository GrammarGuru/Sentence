import requests
import json
from ..pos import POS

with open('../config/api.json') as f:
    URL = json.load(f)['url']

pos_map = {
    'N': POS.Noun,
    'V': POS.Verb,
    'DO': POS.DirectObject,
    'IO': POS.IndirectObject,
    'PN': POS.PredicateNominative,
    'PA': POS.PredicateAdjective
}


def read_pos(tag):
    if type(tag) == int or tag is None:
        return tag
    return pos_map[tag]


def parse(line):
    data = json.loads(requests.post(URL + 'parse', {'text': line}).text)
    pos = [read_pos(tag) for tag in data['pos']]
    return {'doc': data['words'], 'pos': pos}
