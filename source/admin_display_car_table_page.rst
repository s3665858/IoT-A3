Admin's Display Car Table page
=================================
*Directory: app/templates/admin/carlist.html*

The admin's car list page is a html page that displays all information possible available in the Cars 
Table. This information is received from the *cars()* function in :ref:`views`. The admin can modify 
the table with the following:

* Delete a specific car on the table, *deletecar()* is called from :ref:`views`.
* Switch the availablility of the car, either *set_car_availability_to_unavailable()* or *set_car_availability_to_available()* from :ref:`views` will be called depending on the availability.


