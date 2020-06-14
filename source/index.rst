Welcome to IoT A2's documentation!
==================================
Project Summary
----------------
Our project aims to build a car share system. This system is used to book, find and unlock and lock a car.
More details of our project can be found in the IoT Assignment 2 specifications pdf.


Part A 
-------
For part A of our project, we developed a web-based system on MP which includes:

For all users
^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   index_page
   login_page
   register_page

Exclusively for customers
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   customer_home_page
   customer_available_cars_page
   customer_search_car_page
   customer_ongoing_booking_page
   customer_booking_history_page
   customer_google_authentication_page

Exclusively for admins
^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   admin_home_page
   admin_display_car_table_page
   admin_add_car_into_table_page
   admin_display_user_table_page

Our controller functions and classes for Part A
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   views
   main_engine
   user_database_utils
   car_database_utils
   booking_database_utils
   repair_database_utils
   google_calendar_api
   authenticator_runner
   api_authenticator


Part B
-------
For part B of our project, we developed a console-based system on AP which include:
* Receiving credentials of the user who booked the car from MP
* Functionality for user to unlock/return the booked car
* Show the car's location using Google Maps API
The :ref:`client` contains the main() function which provides console UI to the user through AP while 
:ref:`socket_server` is the controller class for it.

.. toctree::
   :maxdepth: 1

   server
   client

Part C
-------
For part C of our project, we have integrated a facial recognition authentication 
into AP so that customers can unlock the car using facial recognition authentication. 
The facial recognition feature is implemented in the :ref:`client` and :ref:`socket_server` 
mentioned in Part B. The :ref:`client` gives the option for the user of unlock the car using 
facial recognition while the :ref:`socket_server` contains the *faceValidation()* function 
which authenticates the user.


Part D
-------
For part D of our project, we implemented unit tests for parts A, B, C of our project.

.. toctree::
   :maxdepth: 1

   test_user_database_utils
   test_car_database_utils
   test_booking_database_utils
   test_mainEngine
   test_server
   

Assignment 3
-------
For the 3rd installment of our project

.. toctree::
   :maxdepth: 1

   pushbullet
   qr
   audio
   
   
 



Indices and tables
==================

* :ref:`search`


.. _index_page:
