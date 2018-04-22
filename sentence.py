import en_core_web_sm
from spacy import displacy
from style import POS

nlp = en_core_web_sm.load()
NOUN_MODIFIERS = {'det', 'amod', 'poss', 'compound', 'nmod', 'cc', 'conj'}
VERB_MODIFIERS = {'aux', 'neg', 'auxpass'}
SUBJECTS = {'nsubj', 'csubj', 'nsubjpass'}
DIRECT_OBJECT = 'dobj'
INDIRECT_OBJECT = 'dative'
PREDICATE_NOMINATIVE = 'attr'
PREDICATE_ADJECTIVE = 'acomp'
PREPOSITION = 'prep'
ROOT = 'ROOT'
PUNCT = 'punct'


class Sentence:
    def __init__(self, s):
        self.doc = nlp(s)
        self.tags = {token.pos_ for token in self.doc}
        self.pos = [None] * len(self.doc)
        self.dict = {token: index for index, token in enumerate(self.doc)}
        self.prep_counter = 0

        self.label(self._get_root)

    def is_valid(self):
        return ('NOUN' in self.tags or 'PROPN' in self.tags) and 'VERB' in self.tags

    def label(self, token):
        index = self.dict[token]
        self.pos[index] = POS.Verb
        for child in token.children:
            if child.dep_ in SUBJECTS:
                self._label_noun(child, tag=POS.Noun)
            elif child.dep_ in VERB_MODIFIERS:
                self._fill(child, POS.Verb, prep=True)
            elif child.dep_ == DIRECT_OBJECT:
                self._label_noun(child, tag=POS.DirectObject)
            elif child.dep_ == INDIRECT_OBJECT:
                self._label_noun(child, tag=POS.IndirectObject)
            elif child.dep_ == PREDICATE_NOMINATIVE:
                self._label_noun(child, tag=POS.PredicateNominative)
            elif child.dep_ == PREDICATE_ADJECTIVE:
                self._fill(child, POS.PredicateAdjective, prep=True)
            elif child.dep_ == PREPOSITION:
                self.prep_counter += 1
                self._label_prep(child)

    @property
    def _get_root(self):
        for token in self.doc:
            if token.dep_ == ROOT:
                return token
        RuntimeError()



    def _label_noun(self, token, tag=POS.Noun):
        index = self.dict[token]
        self.pos[index] = tag
        for child in token.children:
            if child.dep_ in NOUN_MODIFIERS:  # Trivial Labeling
                self._fill(child, tag)
            elif child.dep_ == PREPOSITION:
                self.prep_counter += 1
                self._label_prep(child)

    def _label_prep(self, token):
        index = self.dict[token]
        self.pos[index] = self.prep_counter
        tail = None
        for child in token.children:
            if child.dep_ == PREPOSITION:
                tail = child
            elif child.dep_ != PUNCT:
                self._label_prep(child)

        if tail is not None:
            self.prep_counter += 1
            self._label_prep(tail)

    def _fill(self, token, tag, prep=False):
        index = self.dict[token]
        self.pos[index] = tag
        tail = None
        for child in token.children:
            if prep and child.dep_ == PREPOSITION:
                tail = child
            elif child.dep_ != PUNCT:
                self._fill(child, tag, prep)

        if tail is not None:
            self.prep_counter += 1
            self._label_prep(tail)

    def __str__(self):
        return '{}\n{}'.format(list(self.doc), self.pos)


def test(s):
    doc = nlp(s)
    for token in doc:
        print(token.text, token.dep_, token.head.text, list(token.children))


def display(s):
    doc = nlp(s)
    displacy.serve(doc)


if __name__ == '__main__':
    s = "the man"
    test(s)
    print(Sentence(s))
    display(s)
    while True:
        print(Sentence(input()))
