# Reference: https://docs.python.org/2/library/unittest.html
import unittest
import MySQLdb
from car_database_utils import CarDatabaseUtils

class TestDatabaseUtils(unittest.TestCase):
    HOST = "34.87.224.11"
    USER = "root"
    PASSWORD = "1111"
    DATABASE = "TestData"

    def setUp(self):
        self.connection = MySQLdb.connect(TestDatabaseUtils.HOST, TestDatabaseUtils.USER,
            TestDatabaseUtils.PASSWORD, TestDatabaseUtils.DATABASE)
        
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists Cars")
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
            cursor.execute("insert into Cars (make, body_type, colour, seats, location, cost_per_hour, available) values ('Lamborghini', 'Coupe', 'Orange', 2, 'MelbourneCBD,-37.000.142.000', 5, 1)")
            cursor.execute("insert into Cars (make, body_type, colour, seats, location, cost_per_hour, available) values ('Pajero Sport', 'SUV', 'Black', 7, 'MelbourneCBD,-37.000.142.000', 15, 1)")
            cursor.execute("insert into Cars (make, body_type, colour, seats, location, cost_per_hour, available) values ('Ferrari', 'Coupe', 'Red', 2, 'MelbourneCBD,-37.000.142.000', 10, 1)")
        self.connection.commit()

    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars")
            return cursor.fetchone()[0]

    def countAvailableCars(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where available = 1")
            return cursor.fetchone()[0]

    def countCarsWithMake(self, make):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where lower(make) like %s", ('%' + make + '%',))
            return cursor.fetchone()[0]

    def countCarsWithBodyType(self, bodyType):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where lower(body_type) like %s", ('%' + bodyType + '%',))
            return cursor.fetchone()[0]

    def countCarsWithColour(self, colour):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where lower(colour) like %s", ('%' + colour + '%',))
            return cursor.fetchone()[0]

    def countCarsWithSeats(self, seats):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where seats = %s", (seats,))
            return cursor.fetchone()[0]

    def countCarsWithLocation(self, location):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where lower(location) like %s", ('%' + location + '%',))
            return cursor.fetchone()[0]

    def countCarsWithCost(self, cost):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where cost_per_hour = %s", (cost,))
            return cursor.fetchone()[0]

    def carExists(self, carID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where CarID = %s", (carID,))
            return cursor.fetchone()[0] == 1

    def carIsAvailable(self, carID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where CarID = %s and available = 1", (carID,))
            return cursor.fetchone()[0] == 1

    def carHasLocation(self, carID, location):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where CarID = %s and lower(location) like %s", (carID, '%' + location + '%',))
            return cursor.fetchone()[0] == 1

    def test_insertCar(self):
        with CarDatabaseUtils(self.connection) as db:
            count = self.countCar()
            self.assertTrue(db.insertCar('Lamborghini', 'Coupe', 'Orange', 2, 'MelbourneCBD,-37.000.142.000', 5, 1))
            self.assertTrue(count + 1 == self.countCar())
            self.assertTrue(db.insertCar('Ferrari', 'Coupe', 'Red', 2, 'MelbourneCBD,-37.000.142.000', 15, 1))
            self.assertTrue(count + 2 == self.countCar())

    def test_listCars(self):
        with CarDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countCar() == len(db.listCars()))

    def test_listAvailableCars(self):
        with CarDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countAvailableCars() == len(db.listAvailableCars()))

    def test_searchCarsbyMake(self):
        with CarDatabaseUtils(self.connection) as db:
            make = 'Lamborghini'
            self.assertTrue(self.countCarsWithMake(make) == len(db.searchCarsbyMake(make)))

    def test_searchCarsbyType(self):
        with CarDatabaseUtils(self.connection) as db:
            body_type = 'Coupe'
            self.assertTrue(self.countCarsWithBodyType(body_type) == len(db.searchCarsbyType(body_type)))

    def test_searchCarsbyColour(self):
        with CarDatabaseUtils(self.connection) as db:
            colour = 'Orange'
            self.assertTrue(self.countCarsWithColour(colour) == len(db.searchCarsbyColour(colour)))

    def test_searchCarsbySeats(self):
        with CarDatabaseUtils(self.connection) as db:
            seats = 2
            self.assertTrue(self.countCarsWithSeats(seats) == len(db.searchCarsbySeats(seats)))
    
    def test_searchCarsbyLocation(self):
        with CarDatabaseUtils(self.connection) as db:
            location = 'MelbourneCBD,-37.000.142.000'
            self.assertTrue(self.countCarsWithLocation(location) == len(db.searchCarsbyLocation(location)))

    def test_searchCarsbyCost(self):
        with CarDatabaseUtils(self.connection) as db:
            cost = 5
            self.assertTrue(self.countCarsWithCost(cost) == len(db.searchCarsbyCost(cost)))
    
    def test_deleteCar(self):
        with CarDatabaseUtils(self.connection) as db:
            count = self.countCar()
            carID = 1

            self.assertTrue(self.carExists(carID))

            db.deleteCar(carID)

            self.assertFalse(self.carExists(carID))
            self.assertTrue(count - 1 == self.countCar())

    def test_setCarAvailability(self):
        with CarDatabaseUtils(self.connection) as db:
            carID = 1

            self.assertTrue(self.carExists(carID))
            self.assertTrue(self.carIsAvailable(carID))

            db.setCarAvailability(carID, 0)

            self.assertFalse(self.carIsAvailable(carID))

            db.setCarAvailability(carID, 1)

            self.assertTrue(self.carIsAvailable(carID))

    def test_setCarLocation(self):
        with CarDatabaseUtils(self.connection) as db:
            carID = 1
            location = 'Sydney,-37.000.142.000'

            self.assertTrue(self.carExists(carID))
            self.assertFalse(self.carHasLocation(carID, location))

            db.setCarLocation(carID, location)

            self.assertTrue(self.carHasLocation(carID, location))

if __name__ == "__main__":
    unittest.main()

