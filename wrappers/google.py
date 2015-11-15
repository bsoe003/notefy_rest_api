from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Drive(object):
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)

    def getFiles(self, query):
        try:
            return self.drive.ListFile({'q': query}).GetList()
        except:
            return []

    def download(self, fileID, mimetype="image/jpeg"):
        try:
            self.drive.CreateFile({'id': fileID}).GetContentFile("image_cache/%s.jpg" % fileID, mimetype=mimetype)
            return True
        except:
            return False

    def upload(self, title, content):
        try:
            textFile = self.drive.CreateFile({'title': title})
            textFile.SetContentString(content)
            textFile.Upload()
            return True
        except:
            return False
