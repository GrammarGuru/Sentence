import json

import requests
from nltk import sent_tokenize

from ..pos import POS

with open('config/api.json') as f:
    URL = json.load(f)['url']

pos_map = {
    'N': POS.Noun,
    'V': POS.Verb,
    'DO': POS.DirectObject,
    'IO': POS.IndirectObject,
    'PN': POS.PredicateNominative,
    'PA': POS.PredicateAdjective,
    'APPOS': POS.Appositive,
    'PARTICIPLE': POS.Participle,
    'INF': POS.Infinitive
}


def get_sentences(text):
    return sent_tokenize(text)


def read_pos(tag):
    if type(tag) == int or tag is None:
        return tag
    return pos_map[tag]


def parse_pos(pos):
    return [read_pos(tag) for tag in pos]


def parse_all(lines):
    data = post(URL + 'parseLines', {'lines': lines}).json()
    return [{'doc': line['words'], 'pos': parse_pos(line['pos'])} for line in data]


def parse(line):
    data = post(URL + 'parseLine', {'line': line}).json()
    return {'doc': data['words'], 'pos': parse_pos(data['pos'])}


def filter_lines(lines):
    return post(URL + 'filter', {'lines': lines}).json()


def post(url, body):
    r = requests.post(url, body)
    r.raise_for_status()
    return r
