// Imports the Google Cloud client library
const language = require('@google-cloud/language');

// Instantiates a client
const client = new language.LanguageServiceClient();
const POS = {
    Noun: 'N',
    Verb: 'V',
    DO: 'DO',
    IO: 'IO',
    PN: 'PN',
    PA: 'PA'
}
const NOUN_MODIFIERS = new Set(['DET', 'AMOD', 'POSS', 'CONJ', 'CC', 'PREDET', 'QUANTMOD', 'NN', 'NUM', 'NUMBER']);
const VERB_MODIFIERS = new Set(['AUX', 'NEG', 'AUXPASS', 'ADVMOD']);
const SUBJECTS = new Set(['NSUBJ', 'NSUBJPASS', 'CSUBJ', 'CSUBJPASS', 'EXPL']);
const CLAUSES = new Set(['ADVCL', 'CONJ', 'CCOMP', 'ACL', 'RELCL']);
const DIRECT_OBJECT = new Set(['DOBJ']);
const INDIRECT_OBJECT = new Set(['DATIVE']);
const PREDICATE_NOMINATIVE = new Set(['ATTR']);
const PREDICATE_ADJECTIVE = new Set(['ACOMP']);
const PREPOSITION = 'PREP';
const ROOT = new Set(['ROOT']);
const PUNCT = new Set(['P']);

class Parser {
    constructor(tokens) {
        this.words = new Array(tokens.length);
        this.tags = new Array(tokens.length);
        this.dep = new Array(tokens.length);
        this.parents = new Array(tokens.length);
        this.children = tokens.map(() => []);
        const self = this;
        tokens.forEach((item, index) => {
            self.words[index] = item.text.content;
            self.tags[index] = item.partOfSpeech.tag;
            self.dep[index] = item.dependencyEdge.label;
            self.parents[index] = self.words[item];
            self.children[item.dependencyEdge.headTokenIndex].push(index);
        });
        this.pos = tokens.map(() => null);
        this.prepCounter = 0;

        this.label(this.getRoot());
    }

    getRoot() {
        return this.dep.findIndex(item => item === 'ROOT');
    }

    label(index) {
        const self = this;
        self.pos[index] = POS.Verb;
        self.children[index].forEach(childIndex => {
            const childDep = self.dep[childIndex];
            if(SUBJECTS.has(childDep))
                self.labelNoun(childIndex, POS.Noun);
            else if(VERB_MODIFIERS.has(childDep))
                self.fill(childIndex, POS.Verb, true);
            else if(DIRECT_OBJECT.has(childDep))
                self.labelNoun(childIndex, POS.DO);
            else if(INDIRECT_OBJECT.has(childDep))
                self.labelNoun(childIndex, POS.IO);
            else if(PREDICATE_NOMINATIVE.has(childDep))
                self.labelNoun(childIndex, POS.PN);
            else if(PREDICATE_ADJECTIVE.has(childDep))
                self.fill(childIndex, POS.PA, true);
            else if(childDep === PREPOSITION) {
                self.prepCounter++;
                self.labelPrep(childIndex);
            }
            else if(CLAUSES.has(childDep))
                self.label(childIndex);
        })
    }

    labelNoun(index, tag) {
        this.pos[index] = tag;
        const self = this;
        this.children[index].forEach(childIndex => {
            const childDep = self.dep[childIndex];
            if(NOUN_MODIFIERS.has(childDep))
                self.fill(childIndex, tag);
            else if(childDep === PREPOSITION) {
                self.prepCounter++;
                self.labelPrep(childIndex);
            }
            else if(self.isClause(childIndex))
                self.label(childIndex);

        });
    }

    isClause(index) {
        return this.tags[index] === 'Verb' && CLAUSES.has(this.dep[index]);
    }

    labelPrep(index) {
        this.pos[index] = this.prepCounter;
        let tail = undefined;
        const { dep } = this;
        this.children[index].forEach(childIndex => {
            if(dep[childIndex] === PREPOSITION && dep[index] !== PREPOSITION)
                tail = childIndex;
            else if(dep[childIndex] !== PUNCT)
                this.labelPrep(childIndex);
        })
        if(tail !== undefined) {
            this.prepCounter++;
            this.labelPrep(tail);
        }
    }

    fill(index, tag, checkPrep=false) {
        this.pos[index] = tag;
        let tail = undefined;
        const { dep } = this;
        this.children[index].forEach(childIndex => {
            if(checkPrep && dep[childIndex] === PREPOSITION)
                tail = childIndex;
            else if(dep[childIndex] !== PUNCT)
                this.fill(childIndex, tag, checkPrep);
        })
        if(tail !== undefined) {
            this.prepCounter++;
            this.labelPrep(tail);
        }
    }
}

module.exports = function(req, res) {
    const document = {
        content: req.body.text,
        type: 'PLAIN_TEXT'
    }
    client.analyzeSyntax({ document })
        .then(parsedText => {
            const tokens = parsedText[0].tokens;
            const { words, pos } = new Parser(tokens);
            res.send({ words, pos });
            return { words, pos };
        })
        .catch(err => res.status(422).send(err));
}