#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spelling import Speller

class Formatter(object):
    def __init__(self, dictionary):
        self.speller = Speller(dictionary)

    def formatting(self, text):
        text = text.decode('utf8')
        words = text.split();
        n = len(words)
        for i in range(n):
        	tempWord, termType = "", -1
        	if words[i] == '-' and 0 < i < n:
        		termType = 0
        		tempWord = words[i-1] + words[i+1]
        	elif words[i].startswith('-') and i > 0:
        		termType = 1
        		tempWord = words[i-1] + words[i][1:]
        	elif words[i].endswith('-') and i < len(words):
        		termType = 2
        		tempWord = words[i][:-1] + words[i+1]
        		tempWord = self.speller.correct(tempWord.lower()) if tempWord else ""
        	if tempWord in self.speller.keyterms:
        		if termType == 0:
        			words[i-1] = tempWord
        			words[i] = ""
        			words[i+1] = ""
        		elif termType == 1:
        			words[i-1] = tempWord
        			words[i] = ""
        		elif termType == 2:
        			words[i] = tempWord
        			words[i+1] = ""
        return (" ".join(words)).strip().encode('utf8')

    def setDictionary(self, dictionary):
    	self.speller = Speller(dictionary)

    def prettyPrint(self, text, titleDict):
    	toReturn = "%s\n\n" % text
        for item in titleDict:
        	toReturn += "keyword: %s\nsummary: %s\nurl: %s\n\n" % (item['title'], item['summary'], item['url'])
        return toReturn.strip()

# a = 'The interior contents of cells is the cytoplasm. The cytoplasm is isolated from the surrounding environment by the There are two fundamentally different forms of cells. cells - relatively simple cells - lack nuclear membrane and many Microvilli Plasma membrane — Centriole Lysosome Ribosomes Mitochon- drion Rough endo- Plasmic reticulum Cytoplasm organelles - bacteria and their relatives are all prokaryotic cells - more complex cells - have a nucleus and many organelles - all cells of plants, animals, fungi, and protists Golgi apparatus Cytoskelet n Smooth endoplasmic reticulum Nuclear envelope Nucleolu Nucleus'
# formatter = Formatter("../dictionary/cellFirst10Page.txt")
# text = formatter.formatting(a)
# keywordDict = [{'url': 'https://en.wikipedia.org/wiki/Endoplasmic_reticulum', 
#                'summary': 'The endoplasmic reticulum (ER) is a type of organelle in the cells of eukaryotic organisms that forms an interconnected network of flattened, membrane-enclosed sacs or tube-like structures known as cisternae.', 
#                'title': 'Endoplasmic reticulum'},
#                {'url': 'https://en.wikipedia.org/wiki/Prokaryote',
#                'summary': 'A prokaryote is a single-celled organism that lacks a membrane-bound nucleus (karyon), mitochondria,or any other membrane-bound organelle.', 
#                'title': 'Prokaryote'}]
# print formatter.prettyPrint(text, keywordDict)
