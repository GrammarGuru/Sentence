import os.path

from services.filereaders import pdfreader, wordreader


def read_file(path):
    type = os.path.splitext(path)[1]
    return {
        '.docx': wordreader.read,
        '.pdf': pdfreader.read
    }.get(type, read_default)(path)


def read_default(path):
    with open(path) as f:
        return f.read()
