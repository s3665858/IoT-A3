.. _api_authenticator:

API Authenticator
===================
This function will take in 2 inputs from console input. First being the *userID* and second being the 
*key*. With the correct *key* given this function will be able to create a token file to save 
the user's google calendar account credentials for future use.

main(self)
--------------
function: Takes in an input from the user and passing it to *userID*, then calls *authenticate(userID)*
::

    def main(self):
        userID = input()
        self.authenticate(userID)


authenticate(self, userID)
----------------------------
parameters: *userID*

function: Takes in an authentication key as an input from the user, then verifies it with Google Calendar. 
If the authentication key is correct, creates a token file which stores the user's Google Calendar credentials 
for future use.
::

    def authenticate(self, userID):
        SCOPES = "https://www.googleapis.com/auth/calendar"
        jsonFile = "google_calendar/"+str(userID)+".json"
        store = file.Storage(jsonFile)
        creds = store.get()
        if(not creds or creds.invalid):
            flow = client.flow_from_clientsecrets("google_calendar/credentials.json", SCOPES)
            creds = tools.run_flow(flow, store)

