#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spelling import Speller

class Formatter(object):
    def __init__(self, dictionary):
        self.speller = Speller(dictionary)

    def formatting(self, text):
        refTable = {}
        counter = 1
        text = text.decode('utf8')
        words = text.split();
        n = len(words)
        for i in range(n):
            tempWord, termType = "", -1
            if words[i] == '-' and 0 < i < n-1:
                termType = 0
                tempWord = words[i-1] + words[i+1]
            elif words[i].startswith('-') and i > 0:
                termType = 1
                tempWord = words[i-1] + words[i][1:]
            elif words[i].endswith('-') and i < n-1:
                termType = 2
                tempWord = words[i][:-1] + words[i+1]
                tempWord = self.speller.correct(tempWord.lower()) if tempWord else ""
            if tempWord in self.speller.keyterms:
                if tempWord not in refTable:
                    refTable[tempWord] = counter
                    i = counter
                    counter += 1
                else:
                    i = refTable[tempWord]
                # tempWord += " [%s]" % str(i)
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
        # return {"content": (" ".join(words)).strip().encode('utf8'), "keyterms": refTable}

    def setDictionary(self, dictionary):
        self.speller = Speller(dictionary)

    def prettyPrint(self, text, titleDict, keyterms):
        toReturn = "%s\n\n" % text
        for item in titleDict:
            try:
                index = "[%s] " % str(keyterms.index(item['title'].lower())+1)
                toReturn += index + ("%s\nDefinition: %s\nWikipedia: %s\n\n" % (item['title'], item['summary'], item['url']))
            except:
                continue
        return toReturn.strip()
