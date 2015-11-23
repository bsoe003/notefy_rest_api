from wrappers import spelling
from wrappers.search import Entry
import os
import sqlite3
import wikipedia

conn = sqlite3.connect('keyterms.db')
c = conn.cursor()
try:
	c.execute('''CREATE TABLE entries(title TEXT UNIQUE, summary TEXT, url TEXT UNIQUE)''')
except:
	pass

for dictionary in os.listdir("dictionary"):
    if dictionary.endswith(".txt"):
        speller = spelling.Speller("dictionary/"+dictionary)
        for keyterm in speller.keyterms:
            print "Looking for %s in Wikipedia" % keyterm
            try:
                reference = wikipedia.page(keyterm)
                result = Entry(reference.title, wikipedia.summary(keyterm, sentences=1), reference.url)
            except:
        		print "Search Failure\n"
        		continue
            cmd = "INSERT INTO entries VALUES %s" % ("('"+result.title+"', '"+result.summary+"', '"+result.url+"')")
            print "Inserting %s into Database" % keyterm
            try:
                c.execute(cmd)
                conn.commit()
                print "Successfully inserted: %s\n" % keyterm
            except:
                print "Failed to insert: %s\n" % keyterm
                continue
conn.close()