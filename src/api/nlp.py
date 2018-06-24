import requests
import json
from ..pos import POS

with open('config/api.json') as f:
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


def parse_pos(pos):
    return [read_pos(tag) for tag in pos]


def parse_all(lines):
    data = json.loads(requests.post(URL + 'parseLines', {'lines': lines}).text)
    return [{'doc': line['words'], 'pos': parse_pos(line['pos'])} for line in data]


def parse(line):
    data = json.loads(requests.post(URL + 'parseLine', {'line': line}).text)
    return {'doc': data['words'], 'pos': parse_pos(data['pos'])}
