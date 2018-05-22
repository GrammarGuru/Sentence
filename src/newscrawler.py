from newspaper import Article
import spacy
from .sentence import Sentence

nlp = spacy.load('en_core_web_sm')




if __name__ == '__main__':
    lines = crawl("http://bleacherreport.com/articles/2775757-amanda-nunes-emerges-from-ronda-rouseys-shadow-ready-for-cyborg-fight?utm_source=cnn.com&utm_medium=referral&utm_campaign=editorial")
    for line in lines:
        print(line)