from PyDictionary import PyDictionary

class Word(object):
	def __init__(self, word):
		self.word = word.lower()
		self.synonyms = set()

	def setSynonyms(self, synonyms):
		for synonym in synonyms:
			self.synonyms.add(synonym.lower())

	def __eq__(self, other):
		if isinstance(other, str):
			return self.word == other.lower()
		elif isinstance(other, Word):
			return self.word == other.word and self.synonyms == other.synonyms
		else:
			return False

class Synsets(object):
	def __init__(self, synsets={}): # synsets are hashmap of (string:Word objects) pair
		self.dictionary = PyDictionary()
		self.synsets = synsets

	def find(self, word):
		try:
			return map(str, self.dictionary.synonym(word))
		except:
			if word not in synsets:
				return []
			return synsets[word].synonyms

	def add(self, synsets):
		self.synsets.update(synsets)
