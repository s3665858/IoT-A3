from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pickle

class ApiAuthenticator:
    
    def main(self):
        userID = input()
        self.authenticate(userID)

    def authenticate(self, userID):
        SCOPES = "https://www.googleapis.com/auth/calendar"
        jsonFile = "google_calendar/"+str(userID)+".json"
        store = file.Storage(jsonFile)
        creds = store.get()
        if(not creds or creds.invalid):
            flow = client.flow_from_clientsecrets("google_calendar/credentials.json", SCOPES)
            creds = tools.run_flow(flow, store)
       
ApiAuthenticator().main()