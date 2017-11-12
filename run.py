from Library import Library as Lib
from create import create
from Book import Book
from Article import Article

if __name__ == '__main__':
    lib = Lib()
    for i in range(100):
        lib.add(Article())
    create(lib.generate(['NN', 'VV', 'AJ', 'AV'], 15), 'test.docx')
    print("Done")