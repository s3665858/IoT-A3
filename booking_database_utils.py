import MySQLdb

class BookingDatabaseUtils:
    HOST = "35.244.89.13"
    USER = "root"
    PASSWORD = "1111"
    DATABASE = "Data"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(BookingDatabaseUtils.HOST, BookingDatabaseUtils.USER,
                BookingDatabaseUtils.PASSWORD, BookingDatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

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

    def insertBooking(self, userID, CarID, duration, status):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into Booking (userID, CarID, duration, ongoing) values (%s, %s, %s, %s)", (userID, CarID, duration, status,))
        self.connection.commit()

        return cursor.rowcount == 1

    def listAllBooking(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select BookingID, userID, CarID, duration, ongoing from Booking")
            return cursor.fetchall()
        
    def listCarBookingHistory(self, carID):
        with self.connection.cursor() as cursor:
            cursor.execute("select BookingID, userID, duration, ongoing from Booking WHERE CarID = %s", (carID,))
            return cursor.fetchall()

    def listPersonalBookingHistory(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select BookingID, CarID, duration, ongoing from Booking WHERE userID = %s", (userID,))
            return cursor.fetchall()

    def listPersonalOngoingBooking(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select BookingID, CarID, duration, ongoing from Booking WHERE userID = %s and ongoing = 1", (userID,))
            return cursor.fetchall()
    
    def cancelBooking(self, bookingID):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from Booking where BookingID = %s", (bookingID,))
        self.connection.commit()

        return cursor.rowcount == 1

    def setBookingOngoing(self, bookingID, ongoing):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE Booking SET ongoing = %s where bookingID = %s", (int(ongoing), bookingID,))
        self.connection.commit()
    
    def setBookingDuration(self, bookingID, duration):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE Booking SET duration = %s where bookingID = %s", (duration, bookingID,))
        self.connection.commit()
    
    def getLatestBookingId(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT bookingID FROM Booking ORDER BY bookingID DESC LIMIT 0, 1")
            return cursor.fetchall()
    