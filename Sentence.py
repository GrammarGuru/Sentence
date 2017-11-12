import spacy

nlp = spacy.load('en_core_web_sm')
class Sentence:
    def __init__(self, text):
        if type(text) == list:
            self.text = nlp(' '.join(text))
        else:
            self.text = text
            
        self.tags = []
        for word in text:
            tag = Sentence.convert_tag(word.tag_)
            if tag != None and tag not in self.tags:
                self.tags.append(tag)
                
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