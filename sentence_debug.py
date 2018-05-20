from os import path
from src.newscrawler import crawl
from src.worksheet import Worksheet

FILENAME = 'debug.txt'
LINK = 'http://www.bbc.com/news/world-middle-east-44131466'

if __name__ == '__main__':
    if path.isfile(FILENAME):
        with open(FILENAME) as f:
            lines = [line.strip() for line in f]
    else:
        print("Creating sentences")
        lines = crawl(LINK)
        with open(FILENAME, 'w') as f:
            for line in lines:
                f.write(line)
                f.write('\n')

    Worksheet(lines, key=True).render()