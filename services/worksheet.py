import json
from os import path

from services.utils import post

with open('config/api.json') as f:
    data = json.load(f)
    FUNCTIONS = data['functions']

PUNCT = {',', '.', '-', "'s", "'m", '?', "n't"}

POS_API_MAP = {
    'Subject': 'nounColor',
    'Verb': 'verbColor',
    'PA': 'predicateAdjectiveColor',
    'PN': 'predicateNominativeColor',
    'DO': 'directObjectColor',
    'IO': 'indirectObjectColor',
    'Preposition': 'prepositionColor',
    'Appositive': 'appositiveColor',
    'Participle': 'participleColor',
    'Infinitive': 'infinitiveColor',
}


def create_worksheet(sheet_loc, title, lines, sources, settings):
    key_loc = '{} (Key){}'.format(*path.splitext(sheet_loc))
    body = create_request_body(title, lines, sources, settings)
    response = post(FUNCTIONS + 'worksheet', json=body).content
    sheet, key = tuple(response.split(b', key: '))
    write(sheet_loc, sheet)
    write(key_loc, key)


def create_request_body(title, lines, sources, settings):
    result = {
        'title': title,
        'lines': lines,
        'sources': sources,
        'settings': settings
    }
    with open('config/pos.json') as f:
        pos = json.load(f)

    for name, style in pos.items():
        if style['active']:
            result[POS_API_MAP[name]] = style['rgb']

    return result


def write(loc, content):
    with open(loc, 'wb') as f:
        f.write(content)


if __name__ == '__main__':
    create_worksheet('C:\\Users\\sungo\\Documents\\test.docx',
                     'Worksheet',
                     ['I like cats.'],
                     [],
                     {'Remove Commas': True})
