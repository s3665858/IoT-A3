.. _pushbullet:

Pushbullet API
===================
*Directory: /pushbullet_api.py*

Sends an email to the engineer’s email address using the Pushbullet API when a vehicle
with an issue is reported by an admin.


__init__(self)
--------------
Initializes the Pushbullet API Access token for authentication.



pushNotification(self, carID, car_make)
----------------------------
Stores CarID and Car Make in a dictionary and uses push_note to send a notification 
to admin via Pushbullet API.