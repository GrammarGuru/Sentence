import nltk
import pickle
from nltk.corpus import gutenberg
from Sentence import Sentence

class Book:
    invalids = ['"', ';', '-', '--', '_', "'", '[', ',--']
    def __init__(self, filename):
        self.sentences = []
        self.title = filename[: filename.find(".txt")]
        
        text = gutenberg.sents(filename)
        if ["CHAPTER", "1"] in text:
            text = text[text.index(["CHAPTER", "1"]) + 1 : ]
            
        for sentence in text:
            if not Book.is_valid(sentence):
                continue
            s = Sentence(sentence)
            if 'NN' in s.tags and 'VV' in s.tags:
                self.sentences.append(s)
                
    def is_valid(sentence):
        for character in Book.invalids:
            if character in sentence:
                return False
        return True
    
    def save(self, filename):
        with open(filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

#book = Book("bryant-stories.txt")
#book.save("books.pkl")
#
#with open('books.pkl', 'rb') as file:
#    book = pickle.load(file)
#    print(book.title)
#    for i in book.sentences[0:50]:
#        print(i)