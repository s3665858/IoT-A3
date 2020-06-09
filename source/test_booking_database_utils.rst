Unit Tests for Booking Database Utils
==============================================
This class contains unit test functions for :ref:`booking_database_utils`. Instead of running the queries 
on the actual databse, we run them in *TestData* which is our database for unit testing.

Functions contained in this class:

setUp(self)
---------------
function: Creates the Booking Table in our *TestData* database.
::

    def setUp(self):
        self.connection = MySQLdb.connect(TestDatabaseUtils.HOST, TestDatabaseUtils.USER,
            TestDatabaseUtils.PASSWORD, TestDatabaseUtils.DATABASE)
        
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists Booking")
            cursor.execute("""
                create table if not exists Booking (
                    bookingID int not null auto_increment,
                    userID int not null,
                    CarID int not null,
                    duration text not null,
                    ongoing int not null,
                    constraint PK_Car primary key (bookingID)
                )""")
            cursor.execute("insert into Booking (userID, CarID, duration, ongoing) values (1, 1, '3', 1)")
            cursor.execute("insert into Booking (userID, CarID, duration, ongoing) values (1, 2, '2', 1)")
            cursor.execute("insert into Booking (userID, CarID, duration, ongoing) values (2, 3, '5', 1)")
            cursor.execute("insert into Booking (userID, CarID, duration, ongoing) values (2, 3, '5', 0)")
        self.connection.commit()


tearDown(self)
---------------
function: Closes the connection to the database.
::

    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None


countBooking(self)
---------------------
function: Counts the number of bookings in the database for testing the functions.
::

    def countBooking(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking")
            return cursor.fetchone()[0]


countBookingByID(self, userID)
--------------------------------
parameters: *userID*

function: Counts the number of bookings with value of *userID* being the parameter *userID* 
in the database for testing the functions.
::

    def countBookingByID(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking where userID = %s", (userID,))
            return cursor.fetchone()[0]


countOngoingBookingByID(self, userID)
----------------------------------------
parameters: *userID*

function: Counts the number of bookings with value of *userID* being the parameter *userID* and the 
value *ongoing* being 1 in the database for testing the functions.
::

    def countOngoingBookingByID(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking where userID = %s and ongoing = 1", (userID,))
            return cursor.fetchone()[0]


bookingExists(self, bookingID)
---------------------------------
parameters: *bookingID*

function: Checks if the booking with the *bookingID* parameter given exist in the table.
::

    def bookingExists(self, bookingID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking where bookingID = %s", (bookingID,))
            return cursor.fetchone()[0] == 1


bookingIsOngoing(self, bookingID)
------------------------------------
parameters: *bookingID*

function: Checks if the booking with the *bookingID* parameter given and value *ongoing* being 1 
exist in the table.
::

    def bookingIsOngoing(self, bookingID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking where bookingID = %s and ongoing = 1", (bookingID,))
            return cursor.fetchone()[0] == 1


bookingIsDurationValue(self, bookingID, duration)
----------------------------------------------------
parameters: *bookingID*, *duration*

function: Checks if the booking with the *bookingID* parameter given and value *duration* being the 
*duration* parameter given exist in the table.
::

    def bookingIsDurationValue(self, bookingID, duration):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking where bookingID = %s and duration = %s", (bookingID, duration,))
            return cursor.fetchone()[0] == 1    


test_insertBooking(self)
--------------------------
function: Tests the function *insertBooking()* from :ref:`booking_database_utils`. First it counts the number 
of bookings with *countBooking()*, then adds some bookings into the database and then make sure the counts increases accordingly.
::

    def test_insertBooking(self):
        with BookingDatabaseUtils(self.connection) as db:
            count = self.countBooking()
            self.assertTrue(db.insertBooking(1, 1, '3', 1))
            self.assertTrue(count + 1 == self.countBooking())
            self.assertTrue(db.insertBooking(1, 1, '3', 1))
            self.assertTrue(count + 2 == self.countBooking())


test_listAllBooking(self)
----------------------------
function: Tests the function *listAllBooking()* from :ref:`booking_database_utils`. The test is made by 
comparing the number obtained from *countBooking()* with it.
::

    def test_listAllBooking(self):
        with BookingDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countBooking() == len(db.listAllBooking()))


test_listPersonalBookingHistory(self)
-----------------------------------------
function: Tests the function *listPersonalBookingHistory()* from :ref:`booking_database_utils`. Using a 
test variable of *userID = 1*, the test is made by comparing the number obtained from 
*countBookingByID(userID)* with it.
::

    def test_listPersonalBookingHistory(self):
        userID = 1
        with BookingDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countBookingByID(userID) == len(db.listPersonalBookingHistory(userID)))


test_listPersonalOngoingBooking(self)
-----------------------------------------
function: Tests the function *listPersonalOngoingBooking()* from :ref:`booking_database_utils`. Using a 
test variable of *userID = 1*, the test is made by comparing the number obtained from 
*countOngoingBookingByID(userID)* with it.
::

    def test_listPersonalOngoingBooking(self):
        userID = 1
        with BookingDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countOngoingBookingByID(userID) == len(db.listPersonalOngoingBooking(userID)))


test_cancelBooking(self)
---------------------------
function: Tests the function *cancelBooking()* from :ref:`booking_database_utils`. First it counts the number 
of bookings with *countUser()*, then deletes a booking from the database and then make sure the count decreases by 1.
::

    def test_cancelBooking(self):
        with BookingDatabaseUtils(self.connection) as db:
            count = self.countBooking()
            bookingID = 1

            self.assertTrue(self.bookingExists(bookingID))

            db.cancelBooking(bookingID)

            self.assertFalse(self.bookingExists(bookingID))
            self.assertTrue(count - 1 == self.countBooking())


test_setBookingOngoing(self)
------------------------------
function: Tests the function *setBookingOngoing()* from :ref:`booking_database_utils`. Using a test 
variable of *bookingID = 4*, the *ongoing* value for this car would be initially 0, then set to 1 and check if it works.
::

    def test_setBookingOngoing(self):
        with BookingDatabaseUtils(self.connection) as db:
            bookingID = 4

            self.assertTrue(self.bookingExists(bookingID))
            self.assertFalse(self.bookingIsOngoing(bookingID))

            db.setBookingOngoing(bookingID, 1)

            self.assertTrue(self.bookingIsOngoing(bookingID))

            db.setBookingOngoing(bookingID, 0)

            self.assertFalse(self.bookingIsOngoing(bookingID))


test_setBookingDuration(self)
----------------------------------
function: Tests the function *setBookingDuration()* from :ref:`booking_database_utils`. Using a test 
variable of *bookingID = 4* and *duration = 1*, the *duration* value for this booking would  
initially not equal *duration*, then it would be set to the *duration* value and then check if it was 
changed.
::

    def test_setBookingDuration(self):
        with BookingDatabaseUtils(self.connection) as db:
            bookingID = 4
            duration = 1

            self.assertTrue(self.bookingExists(bookingID))
            self.assertFalse(self.bookingIsDurationValue(bookingID, duration))

            db.setBookingDuration(bookingID, duration)

            self.assertTrue(self.bookingIsDurationValue(bookingID, duration))


