.. _main_engine:

mainEngine.py class
====================
*Directory: /mainEngine.py*

This class functions as our system's controller, the functions within this class calls functions from 
the classes below to manage information in various tables from the database: 

* :ref:`car_database_utils`
* :ref:`user_database_utils`
* :ref:`booking_database_utils`

Functions contained in this class:

__init__(self)
----------------
function: initialises the user, car and booking tables.
::

    def __init__(self):
        self.createUserTable()
        self.createCarTable()
        self.createBookingTable()

createUserTable(self)
-----------------------
function: calls createUserTable() from :ref:`user_database_utils`
::

    def createUserTable(self):
        with UserDatabaseUtils() as db:
            db.createUserTable()

getUser(self, username)
--------------------------
parameters: *username*

function: calls getUser() from :ref:`user_database_utils`. For each user with the same username as *username*, 
returns the user.
::

    def getUser(self, username):
        with UserDatabaseUtils() as db:
            for user in db.getUser():
                if user[1]==username:
                    return user

listUsers(self)
--------------------------
function: calls getUser() from :ref:`user_database_utils`. Returns the entire list of users.
::

    def listUsers(self):
        with UserDatabaseUtils() as db:
            return db.getUser()


register(self, username, password, fname, lname, email)
----------------------------------------------------------
parameters: *username*, *password*, *fname*, *lname*, *email*

function: calls insertUser(*username*, self.hash_password(*password*), *fname*, *lname*, *email*, *'c'*) 
from :ref:`user_database_utils`.
::

    def register(self, username, password, fname, lname, email):
        with UserDatabaseUtils() as db:
            db.insertUser(username, self.hash_password(password), fname, lname, email, 'c')


deleteUser(self, userID)
---------------------------
parameters: *userID*

function: calls deleteUser(userID) from :ref:`user_database_utils`.
::

    def deleteUser(self, userID):
        with UserDatabaseUtils() as db:
            db.deleteUser(userID)


login(self, username, password)
----------------------------------
parameters: *username*, *password*

function: calls getUser() from :ref:`user_database_utils`. From the list of users received, compares 
the username received to the list of users, if a matching username is found, verify the matching user's 
hash password.

::

    def login(self, username, password):
        # constant name and hashed password to imitate stored username and encrypted password
        with UserDatabaseUtils() as db:
            for user in db.getUser():
                find = False
                if user[1]==username and self.verify_password(user[2], password):
                    find = True
                    break
                else:
                    find = False
            return find


hash_password(self, password)
----------------------------------
parameters: *password*

function: creates a salt and transform a password from its text form into a hash.

::

    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        passwordhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        passwordhash = binascii.hexlify(passwordhash)
        return (salt + passwordhash).decode('ascii')


verify_password(self, stored_password, provided_password)
------------------------------------------------------------
parameters: *stored_password*, *provided_password*

function: verifies the *provided_password* from the user by hashing it with the same salt value it was 
originally hashed and compares it with the *stored_password* which is in hash form.

::

    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                      provided_password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password


check_duplicate_username(self, username)
-------------------------------------------
parameters: *username*

function: calls getUser(*username*) from :ref:`user_database_utils`. Checks the entire list of users 
with *username*. Returns true if a match is found, else returns false.

::

    def check_duplicate_username(self, username):
        user=self.getUser(username)
        if user is not None:
            if user[1]==username:
                 return True
        return False # for now


check_isalnum_username(self, username)
-----------------------------------------
parameters: *username*

function: checks if *username* only contains alphanumeric characters using isalnum().

::

    def check_isalnum_username(self, username):
        if username.isalnum():
            return False
        else:
            return True


createCarTable(self)
-----------------------
function: calls createCarTable() from :ref:`car_database_utils`
::

    def createCarTable(self):
        with CarDatabaseUtils() as db:
            db.createCarTable()


listCars(self)
------------------
function: calls listCars() from :ref:`car_database_utils`. Returns the entire list of cars.
::

    def listCars(self):
        with CarDatabaseUtils() as db:
            return db.listCars()


listAvailableCars(self)
---------------------------
function: calls listAvailableCars() from :ref:`car_database_utils`. Returns the entire list of available cars.
::

    def listAvailableCars(self):
        with CarDatabaseUtils() as db:
            return db.listAvailableCars()


insertCar(self, make, body_type, colour, seats, location, cost_per_hour)
---------------------------------------------------------------------------------
paramaters: *make*, *body_type*, *colour*, *seats*, *location*, *cost_per_hour*

function: calls (*make*, *body_type*, *colour*, int(*seats*), *location*, int(*cost_per_hour*), 1) from 
:ref:`car_database_utils`.
::

    def insertCar(self, make, body_type, colour, seats, location, cost_per_hour):
        with CarDatabaseUtils() as db:
            db.insertCar(make, body_type, colour, int(seats), location, int(cost_per_hour), 1)


searchCars(self, column, search)
---------------------------------------
paramaters: *column*, *search*

function: depending on the string value received in *column* call the appropriate search car function in 
:ref:`car_database_utils`.
::

    def searchCars(self, column, search):
        with CarDatabaseUtils() as db:
            if column=="make":
                return db.searchCarsbyMake(search.lower()) #.lower() makes it lowercase
            elif column=="body_type":
                return db.searchCarsbyType(search.lower())   
            elif column=="colour":
                return db.searchCarsbyColour(search.lower())        
            elif column=="seats":
                return db.searchCarsbySeats(search)   
            elif column=="location":
                return db.searchCarsbyLocation(search.lower())
            elif column=="cost":
                return db.searchCarsbyCost(search)


getCar(self, CarID)
----------------------
paramaters: *CarID*

function: calls listCars() from :ref:`car_database_utils`. Search through the list of cars and return 
the car with the matching *CarID*.
::

    def getCar(self, CarID):
        with CarDatabaseUtils() as db:
            for car in db.listCars():
                if car[0]==CarID:
                    return car    


deleteCar(self, CarID)
------------------------
paramaters: *CarID*

function: calls deleteCar(int(*CarID*)) from :ref:`car_database_utils`.
::

    with CarDatabaseUtils() as db:
            db.deleteCar(int(CarID))  


setCarAvailability(self, CarID, Availability)
------------------------------------------------
paramaters: *CarID*, *Availability*

function: calls setCarAvailability(*CarID*, *Availability*) from :ref:`car_database_utils`.
::

    def setCarAvailability(self, CarID, Availability):
        with CarDatabaseUtils() as db:
            db.setCarAvailability(CarID, Availability)


setCarLocation(self, CarID, location)
------------------------------------------------
paramaters: *CarID*, *location*

function: calls setCarLocation(*CarID*, *location*) from :ref:`car_database_utils`.
::

    def setCarLocation(self, CarID, location):
        with CarDatabaseUtils() as db:
            db.setCarLocation(CarID, location)


createBookingTable(self)
----------------------------
function: calls createBookingTable() from :ref:`booking_database_utils`
::

    def createBookingTable(self):
        with BookingDatabaseUtils() as db:
            db.createBookingTable()


insertBooking(self, userID, CarID, duration)
-----------------------------------------------
parameters: *userID*, *CarID*, *duration*

function: calls insertBooking(*userID*, *CarID*, *duration*, 1) from :ref:`booking_database_utils`
::

    def insertBooking(self, userID, CarID, duration):
        with BookingDatabaseUtils() as db:
            db.insertBooking(userID, CarID, duration, 1)


listAllBooking(self)
-----------------------
function: calls listAllBooking() from :ref:`booking_database_utils`. Returns the entire list of bookings.
::

    def listAllBooking(self):
        with BookingDatabaseUtils() as db:
            return db.listAllBooking()


listPersonalBookingHistory(self, userID)
----------------------------------------------
parameters: *userID*

function: calls listPersonalBookingHistory(*userID*) from :ref:`booking_database_utils`. Returns the entire list of personal bookings.
::

    def listPersonalBookingHistory(self, userID):
        with BookingDatabaseUtils() as db:
            return db.listPersonalBookingHistory(userID)


listPersonalOngoingBooking(self, userID)
----------------------------------------------
parameters: *userID*

function: calls listPersonalOngoingBooking(*userID*) from :ref:`booking_database_utils`. Returns the entire list of ongoing bookings.
::

    def listPersonalOngoingBooking(self, userID):
        with BookingDatabaseUtils() as db:
            return db.listPersonalOngoingBooking(userID)


cancelBooking(self, bookingID)
----------------------------------
parameters: *bookingID*

function: calls cancelBooking(*bookingID*) from :ref:`booking_database_utils`.
::

    def cancelBooking(self, bookingID):
        with BookingDatabaseUtils() as db:
            db.cancelBooking(bookingID)


setBookingOngoing(self, bookingID, ongoing)
----------------------------------------------
parameters: *bookingID*, *ongoing*

function: calls setBookingOngoing(*bookingID*, *ongoing*) from :ref:`booking_database_utils`.
::

    def setBookingOngoing(self, bookingID, ongoing):
        with BookingDatabaseUtils() as db:
            db.setBookingOngoing(bookingID, ongoing)


setBookingDuration(self, bookingID, duration)
--------------------------------------------------
parameters: *bookingID*, *duration*

function: calls setBookingDuration(*bookingID*, *duration*) from :ref:`booking_database_utils`.
::

    def setBookingDuration(self, bookingID, duration):
        with BookingDatabaseUtils() as db:
            db.setBookingDuration(bookingID, duration)


getLatestBookingID(self)
--------------------------------------------------
function: calls getLatestBookingId() from :ref:`booking_database_utils`. Returns the first booking ID.
::

    def getLatestBookingID(self):
        with BookingDatabaseUtils() as db:
            for bookingID in db.getLatestBookingId():
                return int(bookingID[0])


createEngineerTable(self)
--------------------------------------------------
Calls createEnginnerTable() from :ref:`engineer_database_utils`

listEngineers(self)
--------------------------------------------------
Calls listAllEngineers() from :ref:`engineer_database_utils`

insertEngineer(self, userID, address)
--------------------------------------------------
Calls insertEngineer() from :ref:`engineer_database_utils`

deleteAddress(self, address)
--------------------------------------------------
Calls deleteAddress() from :ref:`engineer_database_utils`

getEngineerAddress(self, userID)
--------------------------------------------------
Calls createEnginnerTable() from :ref:`engineer_database_utils`

getAllAddress(self)
--------------------------------------------------
Calls getAllAddress() from :ref:`engineer_database_utils`

getAllDetails(self)
--------------------------------------------------
Calls getAllDetails() from :ref:`engineer_database_utils`

getEngineerUserID(self, address)
--------------------------------------------------
Calls getEngineerUserID() from :ref:`engineer_database_utils`

getDurationForGraph(self)
--------------------------------------------------
Calls getTop10Duration() from :ref:`engineer_database_utils`

getTop10Make(self)
--------------------------------------------------
Calls getTop10CarID() from :ref:`engineer_database_utils`

getTop10BookingCountForMake(self)
--------------------------------------------------
Calls getTop10CarIDCount() from :ref:`engineer_database_utils`

getTop10Price(self)
--------------------------------------------------
Calls getTop10Price() from :ref:`engineer_database_utils`

getTop10BookingCountForPrice(self)
--------------------------------------------------
Calls getTop10PriceCount() from :ref:`engineer_database_utils`

getTop10DurationCount(self)
--------------------------------------------------
Calls getTop10DurationCount() from :ref:`engineer_database_utils`

listEngineers(self)
--------------------------------------------------
Calls listAllEngineers() from :ref:`engineer_database_utils`


createRepairTable(self)
--------------------------------------------------
Calls createRepairTable() from :ref:`repair_database_utils`


insertRepair(self, userID, CarID)
--------------------------------------------------
Calls insertRepair() from :ref:`repair_database_utils`.

listPersonalRepairsHistory(self, userID)
--------------------------------------------------
Calls listPersonalRepairsHistory() from :ref:`repair_database_utils`. Returns the entire list of personal repairs history.

listPersonalOngoingRepairs(self, userID)
--------------------------------------------------
Calls listPersonalOngoingRepairs() from :ref:`repair_database_utils`. Returns the entire list of ongoing repairs for engineer.

cancelRepair(self)
--------------------------------------------------
Calls setRepairStatus() from :ref:`repair_database_utils`. Sets repair status to 2 meaning cancelled.

setRepairStatus(self)
--------------------------------------------------
Calls setRepairStatus() from :ref:`repair_database_utils`. Changes repair status.


