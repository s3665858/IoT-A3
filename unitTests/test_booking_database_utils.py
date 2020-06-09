# Reference: https://docs.python.org/2/library/unittest.html
import unittest
import MySQLdb
from booking_database_utils import BookingDatabaseUtils

class TestDatabaseUtils(unittest.TestCase):
    HOST = "34.87.224.11"
    USER = "root"
    PASSWORD = "1111"
    DATABASE = "TestData"

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

    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countBooking(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking")
            return cursor.fetchone()[0]

    def countBookingByID(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking where userID = %s", (userID,))
            return cursor.fetchone()[0]

    def countOngoingBookingByID(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking where userID = %s and ongoing = 1", (userID,))
            return cursor.fetchone()[0]

    def bookingExists(self, bookingID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking where bookingID = %s", (bookingID,))
            return cursor.fetchone()[0] == 1

    def bookingIsOngoing(self, bookingID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking where bookingID = %s and ongoing = 1", (bookingID,))
            return cursor.fetchone()[0] == 1

    def bookingIsDurationValue(self, bookingID, duration):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Booking where bookingID = %s and duration = %s", (bookingID, duration,))
            return cursor.fetchone()[0] == 1      

    def test_insertBooking(self):
        with BookingDatabaseUtils(self.connection) as db:
            count = self.countBooking()
            self.assertTrue(db.insertBooking(1, 1, '3', 1))
            self.assertTrue(count + 1 == self.countBooking())
            self.assertTrue(db.insertBooking(1, 1, '3', 1))
            self.assertTrue(count + 2 == self.countBooking())

    def test_listAllBooking(self):
        with BookingDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countBooking() == len(db.listAllBooking()))

    def test_listPersonalBookingHistory(self):
        userID = 1
        with BookingDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countBookingByID(userID) == len(db.listPersonalBookingHistory(userID)))

    def test_listPersonalOngoingBooking(self):
        userID = 1
        with BookingDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countOngoingBookingByID(userID) == len(db.listPersonalOngoingBooking(userID)))

    def test_cancelBooking(self):
        with BookingDatabaseUtils(self.connection) as db:
            count = self.countBooking()
            bookingID = 1

            self.assertTrue(self.bookingExists(bookingID))

            db.cancelBooking(bookingID)

            self.assertFalse(self.bookingExists(bookingID))
            self.assertTrue(count - 1 == self.countBooking())

    def test_setBookingOngoing(self):
        with BookingDatabaseUtils(self.connection) as db:
            bookingID = 4

            self.assertTrue(self.bookingExists(bookingID))
            self.assertFalse(self.bookingIsOngoing(bookingID))

            db.setBookingOngoing(bookingID, 1)

            self.assertTrue(self.bookingIsOngoing(bookingID))

            db.setBookingOngoing(bookingID, 0)

            self.assertFalse(self.bookingIsOngoing(bookingID))

    def test_setBookingDuration(self):
        with BookingDatabaseUtils(self.connection) as db:
            bookingID = 4
            duration = 1

            self.assertTrue(self.bookingExists(bookingID))
            self.assertFalse(self.bookingIsDurationValue(bookingID, duration))

            db.setBookingDuration(bookingID, duration)

            self.assertTrue(self.bookingIsDurationValue(bookingID, duration))

if __name__ == "__main__":
    unittest.main()
