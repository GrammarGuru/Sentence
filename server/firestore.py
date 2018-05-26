from firebase_admin import firestore
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../config/auth.json'


class FireStore:
    def __init__(self, collection=u'News'):
        self.db = firestore.Client()
        self.collection = self.db.collection(collection)

    def add(self, title, data):
        self.collection.document(title).set(data)

    def get(self, title=None):
        if title is None:
            data = self.collection.get()
            result = {}
            for doc in data:
                result[doc.id] = doc.to_dict()
            return result

        return self.collection.document(title).get().to_dict()


if __name__ == '__main__':
    db = FireStore()
    db.add('me', {
        'Name': 'Beta',
        'DB': "Hello"
    })
    print(db.get())