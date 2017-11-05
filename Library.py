import nltk
import pickle
import random

from Book import Book

class Library:
    def __init__(self):
        self.dict = {}
    
    def add_book(self, book):
        for sentence in book.sentences:
            for tag in sentence.tags:
                if tag not in self.dict:
                    self.dict[tag] = set()
                self.dict[tag].add(sentence)
                
    def save(self, filename):
        with open(filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
            
    def generate(self, tags, amount):
        sentences = set()
        for tag in tags:
            if tag in tags:
                sentences.update(self.dict[tag])
                
        for tag in self.dict.keys():
            if tag not in tags:
                sentences = sentences.difference(self.dict[tag])
                
        return [' '.join(s.text) for s in random.sample(sentences, amount)]
            
        
            
book = Book("bryant-stories.txt")
lib = Library()
lib.add_book(book)
lib.add_book(Book('austen-emma.txt'))
lib.add_book(Book('austen-persuasion.txt'))
lib.add_book(Book('carroll-alice.txt'))
print(lib.generate(['NN', 'VV', 'AJ'], 25))
lib.save("lib.pkl")