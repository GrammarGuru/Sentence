import pickle
import random

from Book import Book

class Library:
    def __init__(self):
        self.dict = {}
    
    def add(self, text):
        for sentence in text.sentences:
            for tag in sentence.tags:
                if tag not in self.dict:
                    self.dict[tag] = set()
                self.dict[tag].add(sentence)
                
    def save(self, filename):
        with open(filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
            
    def generate(self, tags = None, amount = 10):
        sentences = set()
        if tags == None:
            tags = self.dict.keys()
        for tag in tags:
                sentences.update(self.dict[tag])
                

        for tag in self.dict.keys():
            if tag not in tags:
                sentences = sentences.difference(self.dict[tag])
        
        print([s.text for s in sentences])                
        return [str(s.text).strip() for s in random.sample(sentences, min(len(sentences), amount))]