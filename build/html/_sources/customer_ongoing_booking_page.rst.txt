Customer's Ongoing Booking page
==================================
*Directory: app/templates/customer/booking.html*

The customer's ongoing booking page is a html page that displays all ongoing bookings of the current 
user. The ongoing booking information is received from *booking()* function in :ref:`views`. If the user 
cancels a booking on this page, the *deletebooking()* funciton in :ref:`views` will be called.