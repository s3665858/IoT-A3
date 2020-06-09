from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os.path

class GoogleCalendarApi:
    def delete_booking(self, bookingID, userID, make):
        jsonFile = "google_calendar/"+str(userID)+".json"
        store = file.Storage(jsonFile)
        creds = store.get()
        if(not creds or creds.invalid):
            return False
        else:
            service = build("calendar", "v3", http=creds.authorize(Http()))
            eventID = str(100000 + int(bookingID))
            service.events().delete(calendarId = 'primary', eventId = eventID).execute()
            

    def insert_booking(self, bookingID, userID, make, location, duration):
        jsonFile = "google_calendar/"+str(userID)+".json"
        store = file.Storage(jsonFile)
        creds = store.get()
        eventID = str(100000 + int(bookingID))
        if(not creds or creds.invalid):
            return False
        else:
            service = build("calendar", "v3", http=creds.authorize(Http()))
            date = datetime.now()
            start = date.strftime("%Y-%m-%dT%H:%M:%S")
            end = (date + timedelta(days = int(duration))).strftime("%Y-%m-%dT%H:%M:%S")
            time_start = "{}+10:00".format(start)
            time_end = "{}+10:00".format(end)
            event = {
                "summary": "Car BookingID: " + str(bookingID),
                "location": location,
                "id": eventID,
                "description": "Car booking for " + make + ", bookingID: " + str(bookingID),
                "start": {
                    "dateTime": time_start,
                    "timeZone": "Australia/Melbourne",
                },
                "end": {
                    "dateTime": time_end,
                    "timeZone": "Australia/Melbourne",
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        { "method": "email", "minutes": 5 },
                        { "method": "popup", "minutes": 10 },
                    ],
                }
            }
            event = service.events().insert(calendarId = "primary", body = event).execute()
            return True
        
    


