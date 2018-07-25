import json
from enum import Enum

import requests
from nltk import sent_tokenize


class POS(Enum):
    Noun = 0  # Blue
    Verb = 1  # Green
    DirectObject = 2  # Yellow
    IndirectObject = 3  # Orange
    PredicateNominative = 4  # Pink
    PredicateAdjective = 5  # Purple
    PrepositionalPhrase = 6
    Appositive = 7
    Participle = 8
    Infinitive = 9


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


def filter_lines(lines, paragraph_mode=False):
    response = post(URL + 'filter', {'lines': lines}).json()
    if paragraph_mode:
        return [' '.join(lines) for lines in response]
    return [line for lines in response for line in lines]


def post(url, body):
    r = requests.post(url, body)
    r.raise_for_status()
    return r

