Unit Tests for Cars Database Utils
=====================================
This class contains unit test functions for :ref:`car_database_utils`. Instead of running the queries 
on the actual databse, we run them in *TestData* which is our database for unit testing.

Functions contained in this class:

setUp(self)
---------------
function: Creates the Cars Table in our *TestData* database.
::

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


countCar(self)
------------------
function: Counts the number of cars in the database for testing the functions.
::

    def countCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars")
            return cursor.fetchone()[0]


countAvailableCars(self)
---------------------------
function: Counts the number of cars in the database with *available* being 1 for testing the functions.
::

    def countAvailableCars(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where available = 1")
            return cursor.fetchone()[0]


countCarsWithMake(self, make)
--------------------------------
parameters: *make*

function: Counts the number of cars in the database with the make 'like' parameter *make* 
for testing the functions.
::

    def countCarsWithMake(self, make):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where lower(make) like %s", ('%' + make + '%',))
            return cursor.fetchone()[0]


countCarsWithBodyType(self, bodyType)
--------------------------------------
parameters: *bodyType*

function: Counts the number of cars in the database with the body_type 'like' parameter *bodyType* 
for testing the functions.
::

    def countCarsWithBodyType(self, bodyType):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where lower(body_type) like %s", ('%' + bodyType + '%',))
            return cursor.fetchone()[0]


countCarsWithColour(self, colour)
--------------------------------------
parameters: *colour*

function: Counts the number of cars in the database with the colour 'like' parameter *colour* 
for testing the functions.
::

    def countCarsWithColour(self, colour):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where lower(colour) like %s", ('%' + colour + '%',))
            return cursor.fetchone()[0]


countCarsWithSeats(self, seats)
--------------------------------------
parameters: *seats*

function: Counts the number of cars in the database with the colour being parameter *seats* 
for testing the functions.
::

    def countCarsWithSeats(self, seats):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where seats = %s", (seats,))
            return cursor.fetchone()[0]


countCarsWithLocation(self, location)
--------------------------------------
parameters: *location*

function: Counts the number of cars in the database with the location 'like' parameter *location* 
for testing the functions.
::

    def countCarsWithLocation(self, location):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where lower(location) like %s", ('%' + location + '%',))
            return cursor.fetchone()[0]


countCarsWithCost(self, cost)
--------------------------------
parameters: *cost*

function: Counts the number of cars in the database with the cost being parameter *cost* 
for testing the functions.
::

    def countCarsWithCost(self, cost):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where cost_per_hour = %s", (cost,))
            return cursor.fetchone()[0]


carExists(self, carID)
---------------------------
parameters: *carID*

function: Checks if the user with the *carID* parameter given exist in the table.
::

    def carExists(self, carID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where CarID = %s", (carID,))
            return cursor.fetchone()[0] == 1


carIsAvailable(self, carID)
-------------------------------
parameters: *carID*

function: Checks if the user with the *carID* parameter with *availabile* being 1 given exist in the table.
::

    def carIsAvailable(self, carID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where CarID = %s and available = 1", (carID,))
            return cursor.fetchone()[0] == 1


carHasLocation(self, carID, location)
---------------------------------------
parameters: *carID*, *location*

function: Checks if the user with the *carID* parameter has a location 'like' the *location* parameter given exist in the table.
::

    def carHasLocation(self, carID, location):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Cars where CarID = %s and lower(location) like %s", (carID, '%' + location + '%',))
            return cursor.fetchone()[0] == 1


test_insertCar(self)
-----------------------
function: Tests the function *insertCar()* from :ref:`car_database_utils`. First it counts the number 
of cars with *countCar()*, then adds some users into the database and then make sure the counts increases accordingly.
::

    def test_insertCar(self):
        with CarDatabaseUtils(self.connection) as db:
            count = self.countCar()
            self.assertTrue(db.insertCar('Lamborghini', 'Coupe', 'Orange', 2, 'MelbourneCBD,-37.000.142.000', 5, 1))
            self.assertTrue(count + 1 == self.countCar())
            self.assertTrue(db.insertCar('Ferrari', 'Coupe', 'Red', 2, 'MelbourneCBD,-37.000.142.000', 15, 1))
            self.assertTrue(count + 2 == self.countCar())


test_listCars(self)
-----------------------
function: Tests the function *listCars()* from :ref:`car_database_utils`. The test is made by comparing 
the number obtained from *countCar()* with it.
::

    def test_listCars(self):
        with CarDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countCar() == len(db.listCars()))


test_listAvailableCars(self)
------------------------------
function: Tests the function *listAvailableCars()* from :ref:`car_database_utils`. The test is made by comparing 
the number obtained from *countAvailableCars()* with it.
::

    def test_listAvailableCars(self):
        with CarDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countAvailableCars() == len(db.listAvailableCars()))


test_searchCarsbyMake(self)
-------------------------------
function: Tests the function *searchCarsbyMake()* from :ref:`car_database_utils`. The test is made by comparing 
the number obtained from *countCarsWithColour()* with it using a sample variable *make = 'Lamborghini'*.
::

    def test_searchCarsbyMake(self):
        with CarDatabaseUtils(self.connection) as db:
            make = 'Lamborghini'
            self.assertTrue(self.countCarsWithMake(make) == len(db.searchCarsbyMake(make)))


test_searchCarsbyType(self)
-------------------------------
function: Tests the function *searchCarsbyType()* from :ref:`car_database_utils`. The test is made by comparing 
the number obtained from *countCarsWithBodyType()* with it using a sample variable *body_type = 'Coupe'*.
::

    def test_searchCarsbyType(self):
        with CarDatabaseUtils(self.connection) as db:
            body_type = 'Coupe'
            self.assertTrue(self.countCarsWithBodyType(body_type) == len(db.searchCarsbyType(body_type)))


test_searchCarsbyColour(self)
-------------------------------
function: Tests the function *searchCarsbyColour()* from :ref:`car_database_utils`. The test is made by comparing 
the number obtained from *countCarsWithColour()* with it using a sample variable *colour = 'Orange'*.
::

    def test_searchCarsbyColour(self):
        with CarDatabaseUtils(self.connection) as db:
            colour = 'Orange'
            self.assertTrue(self.countCarsWithColour(colour) == len(db.searchCarsbyColour(colour)))


test_searchCarsbySeats(self)
-------------------------------
function: Tests the function *searchCarsbySeats()* from :ref:`car_database_utils`. The test is made by comparing 
the number obtained from *countCarsWithSeats()* with it using a sample variable *seats = 2*.
::

    def test_searchCarsbySeats(self):
        with CarDatabaseUtils(self.connection) as db:
            seats = 2
            self.assertTrue(self.countCarsWithSeats(seats) == len(db.searchCarsbySeats(seats)))


test_searchCarsbyLocation(self)
----------------------------------
function: Tests the function *searchCarsbyLocation()* from :ref:`car_database_utils`. The test is made by comparing 
the number obtained from *countCarsWithLocation()* with it using a sample variable *location = 'MelbourneCBD,-37.000.142.000'*.
::

    def test_searchCarsbyLocation(self):
        with CarDatabaseUtils(self.connection) as db:
            location = 'MelbourneCBD,-37.000.142.000'
            self.assertTrue(self.countCarsWithLocation(location) == len(db.searchCarsbyLocation(location)))


test_searchCarsbyCost(self)
-------------------------------
function: Tests the function *searchCarsbyCost()* from :ref:`car_database_utils`. The test is made by comparing 
the number obtained from *countCarsWithCost()* with it using a sample variable *cost = 5*.
::

    def test_searchCarsbyCost(self):
        with CarDatabaseUtils(self.connection) as db:
            cost = 5
            self.assertTrue(self.countCarsWithCost(cost) == len(db.searchCarsbyCost(cost)))


test_deleteCar(self)
-----------------------
function: Tests the function *deleteCar()* from :ref:`car_database_utils`. First it counts the number 
of cars with *countCar()*, then deletes a car from the database and then make sure the count decreases by 1.
::

    def test_deleteCar(self):
        with CarDatabaseUtils(self.connection) as db:
            count = self.countCar()
            carID = 1

            self.assertTrue(self.carExists(carID))

            db.deleteCar(carID)

            self.assertFalse(self.carExists(carID))
            self.assertTrue(count - 1 == self.countCar())


test_setCarAvailability(self)
------------------------------
function: Tests the function *setCarAvailability()* from :ref:`car_database_utils`. Using a test variable of 
*carID = 1*, the *available* value for this car would be initially 1, then set to 0 and check if it works.
::

    def test_setCarAvailability(self):
        with CarDatabaseUtils(self.connection) as db:
            carID = 1

            self.assertTrue(self.carExists(carID))
            self.assertTrue(self.carIsAvailable(carID))

            db.setCarAvailability(carID, 0)

            self.assertFalse(self.carIsAvailable(carID))

            db.setCarAvailability(carID, 1)

            self.assertTrue(self.carIsAvailable(carID))


test_setCarLocation(self)
------------------------------
function: Tests the function *setCarLocation()* from :ref:`car_database_utils`. Using a test variable of 
*carID = 1* and *location = 'Sydney,-37.000.142.000'*, the *location* value for this car would  
initially not equal *location*, then it would be set to the *location* value and then check if it was changed.
::

    def test_setCarLocation(self):
        with CarDatabaseUtils(self.connection) as db:
            carID = 1
            location = 'Sydney,-37.000.142.000'

            self.assertTrue(self.carExists(carID))
            self.assertFalse(self.carHasLocation(carID, location))

            db.setCarLocation(carID, location)

            self.assertTrue(self.carHasLocation(carID, location))


