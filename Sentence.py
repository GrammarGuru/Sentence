import nltk
from nltk import tokenize

class Sentence:
    def __init__(self, text):
        self.text = text
        self.tags = []
        for tag in nltk.pos_tag(text):
            newTag = Sentence.convert_tag(tag[1])
            if newTag != None and newTag not in self.tags:
                self.tags.append(newTag)
                
    def convert_tag(tag):
        if tag == 'CC':
            return 'CC'
        if tag == 'IN' or tag == 'TO':
            return 'IN'
        sub = tag[0:2]
        if sub == 'NN' or sub == 'PR' or sub == 'WP':
            return 'NN'
        if sub == 'VB':
            return 'VV'
        if sub == 'JJ':
            return 'AJ'
        if sub == 'RB' or tag == 'WRB':
            return 'AV'
        return None
        
    def __str__(self):
        return ' '.join(self.text) + " " + str(self.tags)
    

def convert(sentence):
    return Sentence(sentence, nltk.pos_tag(tokenize(sentence)))