.. _repair_database_utils:

Repair Database Utils class
================
*Directory: repair_database_utils.py*

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
Creates and initialises the repair table


insertRepair(self, userID, CarID, status)
----------------------------------------------------------------------------
Inserts a repair job with the given parameters into the repair table

            
listPersonalRepairsHistory(self, userID)
-----------------
Lists Repairs History for an engineer 


listPersonalOngoingRepairs(self, userID)
---------------------------
Lists the Ongoing repairs for an engineer

setRepairStatus(self, bookingID, status)
---------------------------
Updates the repair status of a car by an engineer
