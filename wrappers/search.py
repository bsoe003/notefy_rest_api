import wikipedia
import base64
import sqlite3

class Entry(object):
    def __init__(self, title, summary, url):
        self.title = str(title)
        self.summary = summary.encode('ascii', 'ignore')
        self.url = str(url)

    def JSON(self):
        return self.__dict__

    def __repr__(self):
        return str(self.JSON())

class Engine(object):
    def __init__(self):
        self.cache = {}

    def find(self, word):
        def checkDB(title):
            conn = sqlite3.connect('keyterms.db')
            cursor = conn.cursor()
            try:
                cursor.execute('''CREATE TABLE entries(title TEXT UNIQUE, summary TEXT, url TEXT UNIQUE)''')
            except:
                pass
            cursor.execute("SELECT * FROM entries WHERE title = ? COLLATE NOCASE", (title,))
            data = cursor.fetchall()
            conn.close()
            return data
        
        def insertDB(entry):
            conn = sqlite3.connect('keyterms.db')
            cursor = conn.cursor()
            try:
                cursor.execute('''CREATE TABLE entries(title TEXT UNIQUE, summary TEXT, url TEXT UNIQUE)''')
            except:
                pass
            cmd = "INSERT INTO entries VALUES %s" % ("('"+entry.lower+"', '"+entry.summary+"', '"+entry.url+"')")
            print bool(cmd)
            cursor.execute(cmd)
            cursor.commit()
            conn.close()
            return entry

        word = word.lower()
        if word in self.cache:
            return self.cache[word]
        # data = checkDB(word)
        # if len(data) > 0:
        #     data = data[0]
        #     entry = Entry(data[0].title(), data[1], data[2])
        #     self.cache[word] = entry
        #     return self.cache[word]
        reference = wikipedia.page(word)
        entry = Entry(reference.title, wikipedia.summary(word, sentences=1), reference.url)
        self.cache[word] = entry
        return self.cache[word]
