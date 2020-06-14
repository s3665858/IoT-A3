.. _google_calendar:

Google Calendar Api class
===========================
This function manages the Google Calendar event related to the car share application of the user.

insert_booking(self, bookingID, userID, make, location, duration)
--------------------------------------------------------------------------
parameters: *bookingID*, *userID*, *make*, *location*, *duration*

function: Creates a Google Calendar event in the user's Google account according to the specified parameters. 
The *eventId* of this event is created by the following function: *str(100000 + int(bookingID))*. This is 
because Google Calendar requires the *eventId* to have at least 6 digits. Since the *bookingID* in our 
system is unique, it is the perfect parameter to be used as the *eventId*.
::

    def insert_booking(self, bookingID, userID, make, location, duration):
        jsonFile = "google_calendar/tokens/"+str(userID)+".json"
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


delete_booking(self, bookingID, userID, make)
--------------------------------------------------
parameters: *bookingID*, *userID*, *make*

function: Deletes a specified car share event from the user's Google Calendar. The *eventId* is obtained 
the same way it was generated in the *insert_booking()* function: *str(100000 + int(bookingID))*.
::

    def delete_booking(self, bookingID, userID, make):
        jsonFile = "google_calendar/tokens/"+str(userID)+".json"
        store = file.Storage(jsonFile)
        creds = store.get()
        if(not creds or creds.invalid):
            return False
        else:
            service = build("calendar", "v3", http=creds.authorize(Http()))
            eventID = str(100000 + int(bookingID))
            service.events().delete(calendarId = 'primary', eventId = eventID).execute()