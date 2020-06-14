.. _engineer_database_utils:

Repair Database Utils class
================
*Directory: engineer_database_utils.py*

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


createEngineerTable(self)
-----------------------
Creates and initializes the Engineer table


insertEngineer(self, userID, CarID, status)
----------------------------------------------------------------------------
Inserts an engineer with the given parameters into the Engineer table


deleteAddress(self, userID)
-----------------
Deletes the address row in the Engineer table where the engineerID column has the same value to the parameter engineerID.

listAllEngineers(self, userID)
---------------------------
Query for all the rows in the Engineer table


getEngineerAddress(self, bookingID, status)
---------------------------
Query for the all the rows in the Engineer table 

getEngineerUserID(self, bookingID, status)
---------------------------
Query for the userID type of all the rows in the Engineer table where the userID column has the same value to the parameter UserID.