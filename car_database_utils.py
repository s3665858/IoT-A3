import MySQLdb

class CarDatabaseUtils:
    HOST = "34.87.224.11"
    USER = "root"
    PASSWORD = "1111"
    DATABASE = "Data"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(CarDatabaseUtils.HOST, CarDatabaseUtils.USER,
                CarDatabaseUtils.PASSWORD, CarDatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

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

    def insertCar(self, make, body_type, colour, seats, location, cost_per_hour, availability):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into Cars (make, body_type, colour, seats, location, cost_per_hour, available) values (%s, %s, %s, %s, %s, %s, %s)", (make, body_type, colour, seats, location, cost_per_hour,availability,))
        self.connection.commit()

        return cursor.rowcount == 1

    def listCars(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars")
            return cursor.fetchall()

    def listAvailableCars(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE available = 1")
            return cursor.fetchall()

    def searchCarsbyMake(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE lower(make) like %s", ('%' +search + '%',))
            return cursor.fetchall()

    def searchCarsbyType(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE lower(body_type) like %s", ('%' +search + '%',))
            return cursor.fetchall()

    def searchCarsbyColour(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE lower(colour) like %s", ('%' +search + '%',))
            return cursor.fetchall()
        
    def searchCarsbySeats(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE seats = %s", (search,))
            return cursor.fetchall()

    def searchCarsbyLocation(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE lower(location) like %s", ('%' +search + '%',))
            return cursor.fetchall()

    def searchCarsbyCost(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Cars WHERE cost_per_hour = %s", (search,))
            return cursor.fetchall()

    def deleteCar(self, CarID):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from Cars where CarID = %s", (CarID,))
        self.connection.commit()

        return cursor.rowcount == 1

    def setCarAvailability(self, CarID, Availability):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE Cars SET available = %s WHERE CarID = %s", (int(Availability), CarID,))
        self.connection.commit()
        
    def setCarLocation(self, CarID, location):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE Cars SET location = %s WHERE CarID = %s", (location, CarID,))
        self.connection.commit()
    

