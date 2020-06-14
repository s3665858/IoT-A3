.. _repair_database_utils:

Repair Database Utils class
================
*Directory: app/templates/register.html*

This class manages the *Repair* Table in our database *Data* by executing MySQL the appropriate queries.

__init__(self, connection = None)
---------------------------------------------
If a connection is not established, establish a connection on MySQLdb with our private credentials.


close(self)
--------------
Closes the connection with the database.


__enter__(self)
----------------
Return the class itself.


__exit__(self, type, value, traceback)
------------------------------------------------
Executes close()


createRepairTable(self)
-----------------------
Creates and initialises the User table


insertRepair(self, userID, CarID, status)
----------------------------------------------------------------------------
Inserts a user with the given parameters into the User table

            

listPersonalRepairsHistory(self, userID)
-----------------
Query for the userID, username, password, firstname, lastname, email, type of all the rows 
in the User table


listPersonalOngoingRepairs(self, userID)
---------------------------
Deletes the row in the User table where the *userID* column has the same value to 
the parameter *UserID*.

setRepairStatus(self, bookingID, status)
---------------------------
Deletes the row in the User table where the *userID* column has the same value to 
the parameter *UserID*.
