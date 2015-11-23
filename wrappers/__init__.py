import google, search, formatter
import os
import requests

class Notefy(object):
    def __init__(self, dictionary=""):
        self.drive = google.Drive()
        self.engine = search.Engine()
        # self.speller = None
        self.sf = formatter.Formatter(dictionary)
        self.input = ""

    def download(self, filename):
        filelist = self.drive.getFiles("title = '%s'" % (filename+".jpg"))
        if not filelist:
            return {"error": "%s does not exist in your drive" % filename}
        fileID = filelist[0]['id']
        self.input = "image_cache/%s.jpg" % fileID
        print "Attempting to download: %s.jpg" % fileID
        if not self.drive.download(fileID):
            return {"error": "There seems to be an error while downloading"}
        print "Download Complete!"
        return {}

    def upload(self, title, content):
        print "Attempting to upload OCR result"
        if not self.drive.upload(title, content):
            return {"error": "There seems to be an error while uploading"}
        print "Upload Complete!"
        return {}

    def sendToOCR(self):
        data = {"apikey": "helloworld", "language": "eng"}
        files = {"file": open(os.getcwd()+"/"+self.input, 'rb')}
        response = requests.post("https://ocr.a9t9.com/api/Parse/Image", data=data, files=files)
        # print "\nOCR Result:\n"+unicode(response.json()["ParsedResults"][0]["ParsedText"])
        return response.json()["ParsedResults"][0]["ParsedText"]

    def isKeyterm(self, word):
        if not self.sf.speller:
            return False
        for key in self.sf.speller.keyterms:
            if word.lower().strip() in key.split():
                return True
        return False

    def clean(self):
        try:
            os.remove(self.input)
        except:
            pass
