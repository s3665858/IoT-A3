.. _car_database_utils:

Car Database Utils class
==========================
This class manages the *Cars* Table in our database *Data* by executing MySQL the appropriate queries.

Functions contained in this class:

__init__(self, connection = None)
---------------------------------------------
parameters: connection

function: If a connection is not established, establish a connection on MySQLdb with our private credentials.
::

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(CarDatabaseUtils.HOST, CarDatabaseUtils.USER,
                CarDatabaseUtils.PASSWORD, CarDatabaseUtils.DATABASE)
        self.connection = connection


close(self)
--------------
function: Closes the connection with the database.
::

    def close(self):
        self.connection.close()


__enter__(self)
----------------
function: Return the class itself.
::

    def __enter__(self):
        return self


__exit__(self, type, value, traceback)
------------------------------------------------
function: Executes close()
::

    def __exit__(self, type, value, traceback):
        self.close()


createCarTable(self)
-----------------------
function: Creates and initialises the Cars table
::

    def createCarTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Cars (
                    CarID int not null auto_increment,
                    make text not null,
                    body_type text not null,
                    colour text not null,
                    seats int not null,
                    location text not null,
                    cost_per_hour int not null,
                    available int not null,
                    constraint PK_Car primary key (CarID)
                )""")
        self.connection.commit()


insertCar(self, make, body_type, colour, seats, location, cost_per_hour, availability)
--------------------------------------------------------------------------------------------
parameters: *make*, *body_type*, *colour*, *seats*, *location*, *cost_per_hour*, *availability*

function: Inserts a car with the given parameters into the Cars table
::

    def insertCar(self, make, body_type, colour, seats, location, cost_per_hour, availability):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into Cars (make, body_type, colour, seats, location, cost_per_hour, available) values (%s, %s, %s, %s, %s, %s, %s)", (make, body_type, colour, seats, location, cost_per_hour,availability,))
        self.connection.commit()

        return cursor.rowcount == 1


listCars(self)
-----------------
function: Query for all the rows in the Cars table
::

    def listCars(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars")
            return cursor.fetchall()


listAvailableCars(self)
--------------------------
function: Query for all the rows in the Cars table where the *avaiable* column contains the value 1 (1 means that the car is available)
::

    def listAvailableCars(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE available = 1")
            return cursor.fetchall()


searchCarsbyMake(self, search)
--------------------------------
parameters: *search*

function: Query for all the rows in the Cars table where the *make* column has a similar value to *search* 
using the *LIKE* keyword
::

    def searchCarsbyMake(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE lower(make) like %s", ('%' +search + '%',))
            return cursor.fetchall()


searchCarsbyType(self, search)
--------------------------------
parameters: *search*

function: Query for all the rows in the Cars table where the *body_type* column has a similar value to *search* 
using the *LIKE* keyword
::

    def searchCarsbyType(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE lower(body_type) like %s", ('%' +search + '%',))
            return cursor.fetchall()


searchCarsbyColour(self, search)
-----------------------------------
parameters: *search*

function: Query for all the rows in the Cars table where the *colour* column has a similar value to *search* 
using the *LIKE* keyword
::

    def searchCarsbyColour(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE lower(colour) like %s", ('%' +search + '%',))
            return cursor.fetchall()


searchCarsbySeats(self, search)
-----------------------------------
parameters: *search*

function: Query for all the rows in the Cars table where the *seats* column has the same value to *search*.
::

    def searchCarsbySeats(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE seats = %s", (search,))
            return cursor.fetchall()


searchCarsbyLocation(self, search)
-----------------------------------
parameters: *search*

function: Query for all the rows in the Cars table where the *location* column has a similar value to *search* 
using the *LIKE* keyword
::

    def searchCarsbyLocation(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE lower(location) like %s", ('%' +search + '%',))
            return cursor.fetchall()


searchCarsbyCost(self, search)
-----------------------------------
parameters: *search*

function: Query for all the rows in the Cars table where the *cost_per_hour* column has the same value to *search*.
::

    def searchCarsbyCost(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE cost_per_hour = %s", (search,))
            return cursor.fetchall()


deleteCar(self, CarID)
-----------------------------------
parameters: *CarID*

function: Deletes the row in the Cars table where the *CarID* column has the same value to 
the parameter *CarID*.
::

    def deleteCar(self, CarID):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from Cars where CarID = %s", (CarID,))
        self.connection.commit()

        return cursor.rowcount == 1


setCarAvailability(self, CarID, Availability)
------------------------------------------------
parameters: *CarID*, *Availability*

function: Updates the *available* column of the Cars table to the parameter *Availability* on the row where 
*CarID* column equals to the parameter *CarID*.
::

    def setCarAvailability(self, CarID, Availability):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE Cars SET available = %s WHERE CarID = %s", (int(Availability), CarID,))
        self.connection.commit()


setCarLocation(self, CarID, location)
-----------------------------------------
parameters: *CarID*, *location*

function: Updates the *location* column of the Cars table to the parameter *location* on the row where 
*CarID* column equals to the parameter *CarID*.
::

    def setCarLocation(self, CarID, location):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE Cars SET location = %s WHERE CarID = %s", (location, CarID,))
        self.connection.commit()
