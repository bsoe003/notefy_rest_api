import httplib2
import os
import time

from apiclient import discovery, errors, http
from oauth2client import client, tools
import oauth2client

CLIENT_SECRET = "client_secret.json"
APPLICATION_NAME = "Notefy"
SCOPE = "https://www.googleapis.com/auth/drive"

class Drive(object):
    def __init__(self):
        self.credentials = self.getCredentials()
        self.service = discovery.build('drive', 'v2', http=self.credentials.authorize(httplib2.Http()))

    def getCredentials(self):
        directory = {}
        directory["home"] = os.path.expanduser('~')
        directory["credential"] = os.path.join(directory["home"], ".credentials")
        if not os.path.exists(directory["credential"]):
            os.makedirs(directory["credential"])
        path = os.path.join(directory["credential"], "notefy.json")
        store = oauth2client.file.Storage(path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPE)
            flow.user_agent = APPLICATION_NAME
            try:
                import argparse
                flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
                credentials = tools.run_flow(flow, store, flags)
            except ImportError:
                flags = None
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + path)
        return credentials

    def retrieveFiles(self, mimeType):
        result = []
        token = None
        while True:
            try:
                param = {}
                if token:
                    param["pageToken"] = token
                files = self.service.files().list(**param).execute()
                for item in files["items"]:
                    if item["mimeType"] == mimeType:
                        result.append(item)
                token = files.get('nextPageToken')
                if not token:
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break
        return result

    def download(self, fileID, destination):
        request = self.service.files().get_media(fileId=fileID)
        media_request = http.MediaIoBaseDownload(destination, request)
        while True:
            try:
                download_progress, done = media_request.next_chunk()
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                return
            if download_progress:
                print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
            if done:
                print 'Download Complete'
                return

drive = Drive()
# print drive.retrieveFiles("image/jpeg")
# drive.download("0B8BpS6HWrs1RZld1YnhwaFhJMjQ", open("tmp.jpg", "w"))
