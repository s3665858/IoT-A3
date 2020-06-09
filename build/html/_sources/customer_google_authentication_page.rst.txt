.. _google_authentication_page:

Google Authentication page
===========================
*Directory: app/templates/customer/googleAuthentication.html*

A customer would only be directed to the Google Authentication page if the system does not have 
permissions to access the Google Calendar of the customer's google account. The page would ask the 
customer to go to a link to allow permissions to their google account's Google Calendar, then asks 
the user to provide the authentication key provided by that link. The key received from the user 
would then call the *googleAuthenticate()* function in :ref:`views` which then displays a success message 
if the authentication succeeded.