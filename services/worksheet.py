import json
from os import path

import requests

with open('config/api.json') as f:
    data = json.load(f)
    URL = data['url']
    FUNCTIONS = data['local']

PUNCT = {',', '.', '-', "'s", "'m", '?', "n't"}


def create_worksheet(sheet_loc, title, lines, sources, settings):
    key_loc = '{} (Key){}'.format(*path.splitext(sheet_loc))
    lines = requests.post(URL + 'parseLines', {'lines': lines}).json()
    with open('config/pos.json') as f:
        pos = json.load(f)
    print(lines)
    response = requests.post(FUNCTIONS + 'worksheet', json={
        'title': title,
        'sources': sources,
        'removeCommas': settings['Remove Commas'],
        'lines': lines,
        'pos': pos
    }).content

    sheet, key = tuple(response.split(b', '))
    write(sheet_loc, sheet)
    write(key_loc, key)


def write(loc, content):
    with open(loc, 'wb') as f:
        f.write(content)


if __name__ == '__main__':
    create_worksheet('C:\\Users\\sungo\\Documents\\test.docx',
                     'Worksheet',
                     ['I like cats.'],
                     [],
                     {'Remove Commas': True})
