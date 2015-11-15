import wikipedia
import base64

class Entry(object):
    def __init__(self, title, summary, url):
        self.title = str(title)
        self.summary = summary.encode('ascii', 'ignore')
        self.url = str(url)

    def JSON(self):
        return self.__dict__

    def __repr__(self):
        return str(self.JSON())

class Pedia(object):
    def __init__(self):
        self.cache = {}

    def find(self, word):
        word = word.lower()
        if word in self.cache:
            return self.cache[word]
        reference = wikipedia.page(word)
        entry = Entry(reference.title, wikipedia.summary(word, sentences=1), reference.url)
        self.cache[word] = entry
        return self.cache[word]
