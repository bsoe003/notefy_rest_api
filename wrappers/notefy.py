import google, wiki
import os
import requests

class Notefy(object):
    def __init__(self):
        self.drive = google.Drive()
        self.pedia = wiki.Pedia()
        self.input = ""
        self.output = ""

    def download(self, fileID):
        self.input = "image_cache/"+fileID+".jpg"
        if not self.drive.download(fileID, open(self.input, 'w')):
            return {"error": "There seems to be an error while downloading"}
        return {}

    def upload(self, title, mimeType):
        if not self.drive.upload(title, "", "text/plain", self.output):
            return {"error": "There seems to be an error while uploading"}
        return {}

    def setOutput(self, filename, content):
        f = open(filename, 'w')
        f.write(content)
        f.close()
        self.output = filename

    def sendToOCR(self):
        data = {"apikey": "helloworld", "language": "eng"}
        files = {"file": open(os.getcwd()+"/"+self.input, 'rb')}
        response = requests.post("https://ocr.a9t9.com/api/Parse/Image", data=data, files=files)
        print "\nOCR Result:\n"+str(response.json()["ParsedResults"][0]["ParsedText"])
        return response.json()["ParsedResults"][0]["ParsedText"]

    def clean(self):
        try:
            os.remove(self.input)
        except:
            pass
        try:
            os.remove(self.output)
        except:
            pass