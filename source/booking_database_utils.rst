.. _booking_database_utils:

Booking Database Utils class
==============================
This class manages the *Booking* Table in our database *Data* by executing MySQL the appropriate queries.

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


createBookingTable(self)
---------------------------
function: Creates and initialises the Booking table
::

    def createBookingTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Booking (
                    bookingID int not null auto_increment,
                    userID int not null,
                    CarID int not null,
                    duration text not null,
                    ongoing int not null,
                    constraint PK_Car primary key (bookingID)
                )""")
        self.connection.commit()


insertBooking(self, userID, CarID, duration, status)
-------------------------------------------------------
parameters: *userID*, *CarID*, *duration*, *status*

function: Inserts a booking with the given parameters into the Booking table
::

    def insertBooking(self, userID, CarID, duration, status):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into Booking (userID, CarID, duration, ongoing) values (%s, %s, %s, %s)", (userID, CarID, duration, status,))
        self.connection.commit()

        return cursor.rowcount == 1


listAllBooking(self)
----------------------
function: Query for the *BookingID*, *userID*, *CarID*, *duration* and *ongoing* of all the rows in the Booking table
::

    def listAllBooking(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select BookingID, userID, CarID, duration, ongoing from Booking")
            return cursor.fetchall()


listPersonalBookingHistory(self, userID)
------------------------------------------
parameters: *userID*

function: Query for the *BookingID*, *userID*, *CarID*, *duration* and *ongoing* of all the rows in the Booking table 
where the column *userID* equals to the parameter *userID*.
::

    def listPersonalBookingHistory(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select BookingID, CarID, duration, ongoing from Booking WHERE userID = %s", (userID,))
            return cursor.fetchall()


listPersonalOngoingBooking(self, userID)
--------------------------------------------
parameters: *userID*

function: Query for the *BookingID*, *userID*, *CarID*, *duration* and *ongoing* of all the rows in the Booking table 
where the column *userID* equals to the parameter *userID* and the column *ongoing* equals to 1 (1 means the booking is ongoing).
::

    def listPersonalOngoingBooking(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select BookingID, CarID, duration, ongoing from Booking WHERE userID = %s and ongoing = 1", (userID,))
            return cursor.fetchall()



cancelBooking(self, bookingID)
-----------------------------------
parameters: *bookingID*

function: Deletes the row in the Booking table where the *BookingID* column has the same value to 
the parameter *bookingID*.
::

    def cancelBooking(self, bookingID):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from Booking where BookingID = %s", (bookingID,))
        self.connection.commit()

        return cursor.rowcount == 1


setBookingOngoing(self, bookingID, ongoing)
------------------------------------------------
parameters: *bookingID*, *ongoing*

function: Updates the *ongoing* column of the Cars table to the parameter *ongoing* on the row where 
*bookingID* column equals to the parameter *bookingID*.
::

    def setBookingOngoing(self, bookingID, ongoing):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE Booking SET ongoing = %s where bookingID = %s", (int(ongoing), bookingID,))
        self.connection.commit()


setBookingDuration(self, bookingID, duration)
-----------------------------------------------
parameters: *bookingID*, *duration*

function: Updates the *duration* column of the Cars table to the parameter *duration* on the row where 
*bookingID* column equals to the parameter *bookingID*.
::

    def setBookingDuration(self, bookingID, duration):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE Booking SET duration = %s where bookingID = %s", (duration, bookingID,))
        self.connection.commit()


getLatestBookingId(self)
-----------------------------------------------
function: Query the database for the latest *bookingID* by arranging it to descending order and getting the 
*bookingID* at first row.
::

    def getLatestBookingId(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT bookingID FROM Booking ORDER BY bookingID DESC LIMIT 0, 1")
            return cursor.fetchall()
