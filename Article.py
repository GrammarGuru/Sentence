import spacy
import pickle
from Sentence import Sentence
import wikipedia

class Article:
    nlp = spacy.load('en_core_web_sm')
    def __init__(self, title = None):
        if title == None:
            page = None
            while page == None:
                try:
                    self.title = wikipedia.random()
                    page = wikipedia.summary(self.title)
                except:
                    pass
        else:
            self.title = title
            page = wikipedia.summary(self.title)
        
        text = Article.nlp(page).sents
        self.sentences = []
        for line in text:
            s = Sentence(line)
            if 'NN' in s.tags and 'VV' in s.tags and len(line) > 0:
                self.sentences.append(s)
        
    def save(self, filename = None):
        if filename == None:
            filename = self.title + '.pkl'
        with open(filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
