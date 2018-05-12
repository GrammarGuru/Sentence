from os import path
from newscrawler import crawl
from worksheet import Worksheet

FILENAME = 'debug.txt'
LINK = 'https://abcnews.go.com/International/wireStory/monitor-42-killed-israeli-strikes-syria-week-55115848'

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

    Worksheet(lines).render(key=True)