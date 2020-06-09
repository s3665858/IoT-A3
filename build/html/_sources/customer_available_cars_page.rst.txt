Customer's Car List page
================================
*Directory: app/templates/customer/carlist.html*

The customer's car list page is a html page that displays all the cars which are available for booking 
to the current user. The car list information is received from *cars()* function in :ref:`views`. 
If the user books a car here, the *makebooking()* function in :ref:`views` would then be called. If 
the user has not allowed the system permissions to their Google Calendar yet, the user would then be 
directed to the :ref:`google_authentication_page`.

