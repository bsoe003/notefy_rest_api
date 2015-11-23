import re, collections
import os

alphabet = 'abcdefghijklmnopqrstuvwxyz'

class Speller(object):
    def __init__(self, database):
        def words(texts):
            terms = []
            for text in texts:
                text = text.strip()
                if not text:
                    continue
                terms.append(text.lower())
            return list(terms)
            # return re.findall('[a-z]+', text.lower())
        self.keyterms = self.train(words(file(database).readlines()))
        print self.keyterms

    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def correct(self, word):
        def edits1(word):
            s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
            deletes    = [a + b[1:] for a, b in s if b]
            transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
            replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
            inserts    = [a + c + b     for a, b in s for c in alphabet]
            return set(deletes + transposes + replaces + inserts)

        def known_edits2(word):
            return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in self.keyterms)

        def known(words):
            return set(w for w in words if w in self.keyterms)

        candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
        return max(candidates, key=self.keyterms.get)

# speller = Speller(os.getcwd()+'/../big.txt')
# print speller.correct("speling")
