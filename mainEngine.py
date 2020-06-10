import hashlib, binascii, os
from user_database_utils import UserDatabaseUtils
from car_database_utils import CarDatabaseUtils
from booking_database_utils import BookingDatabaseUtils

class MainEngine:
    def __init__(self):
        self.createUserTable()
        self.createCarTable()
        self.createBookingTable()
        
    def createUserTable(self):
        with UserDatabaseUtils() as db:
            db.createUserTable()
    
    def getUser(self, username):
        with UserDatabaseUtils() as db:
            for user in db.getUser():
                if user[1]==username:
                    return user

    def listUsers(self):
        with UserDatabaseUtils() as db:
            return db.getUser()
            
    def register(self, username, password, fname, lname, email):
        with UserDatabaseUtils() as db:
            db.insertUser(username, self.hash_password(password), fname, lname, email, 'c')
    
    def deleteUser(self, userID):
        with UserDatabaseUtils() as db:
            db.deleteUser(userID)
    
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
        
    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        passwordhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        passwordhash = binascii.hexlify(passwordhash)
        return (salt + passwordhash).decode('ascii')

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

    # return False if no duplicates
    def check_duplicate_username(self, username):
        user=self.getUser(username)
        if user is not None:
            if user[1]==username:
                 return True
        return False # for now
    
    def searchUsers(self, column, search):
        with UserDatabaseUtils() as db:
            if column=="username":
                return db.searchUsersbyUsername(search.lower()) #.lower() makes it lowercase
            elif column=="firstname":
                return db.searchUsersbyFirstName(search.lower())   
            elif column=="lastname":
                return db.searchUsersbyLastName(search.lower())        
            elif column=="email":
                return db.searchUsersbyEmail(search.lower())   
            elif column=="type":
                account_type='z'
                if search == "admin":
                    account_type='a'
                elif search == "customer":
                    account_type='c'
                elif search == "engineer":
                    account_type='e'
                elif search == "manager":
                    account_type='m'
                return db.searchUsersbyType(account_type)

    # return False if isalnum
    def check_isalnum_username(self, username):
        if username.isalnum():
            return False
        else:
            return True

    ### functions for managing car tables ###
    def createCarTable(self):
        with CarDatabaseUtils() as db:
            db.createCarTable()
            
    #user input to be transferred to ManagerView and CustomerView when sean feels like it
    def listCars(self):
        with CarDatabaseUtils() as db:
            return db.listCars()
        
    def listAvailableCars(self):
        with CarDatabaseUtils() as db:
            return db.listAvailableCars()

    def insertCar(self, make, body_type, colour, seats, location, cost_per_hour):
        with CarDatabaseUtils() as db:
            db.insertCar(make, body_type, colour, int(seats), location, int(cost_per_hour), 1)
    
    def updateCar(self, carID, name, bodytype, colour, seats, location, cost, availibility):
        with CarDatabaseUtils() as db:
            db.updateCar(carID, name, bodytype, colour, int(seats), location, int(cost), int(availibility))
        
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

    def getCar(self, CarID):
        with CarDatabaseUtils() as db:
            for car in db.listCars():
                if car[0]==CarID:
                    return car            

    def getCarDetails(self, CarID):
        with CarDatabaseUtils() as db:
            return db.getCarDetails(int(CarID))

    def deleteCar(self, CarID):
        with CarDatabaseUtils() as db:
            db.deleteCar(int(CarID))

    def setCarAvailability(self, CarID, Availability):
        with CarDatabaseUtils() as db:
            db.setCarAvailability(CarID, Availability)

    def setCarLocation(self, CarID, location):
        with CarDatabaseUtils() as db:
            db.setCarLocation(CarID, location)

    ### functions for managing booking history tables ###
    def createBookingTable(self):
        with BookingDatabaseUtils() as db:
            db.createBookingTable()

    def insertBooking(self, userID, CarID, duration):
        with BookingDatabaseUtils() as db:
            db.insertBooking(userID, CarID, duration, 1)

    def listAllBooking(self):
        with BookingDatabaseUtils() as db:
            return db.listAllBooking()
            
    def listPersonalBookingHistory(self, userID):
        with BookingDatabaseUtils() as db:
            return db.listPersonalBookingHistory(userID)
    
    def listCarBookingHistory(self, carID):
        with BookingDatabaseUtils() as db:
            return db.listCarBookingHistory(carID)
    
    def listPersonalOngoingBooking(self, userID):
        with BookingDatabaseUtils() as db:
            return db.listPersonalOngoingBooking(userID)


    def cancelBooking(self, bookingID):
        with BookingDatabaseUtils() as db:
            db.cancelBooking(bookingID)

    def setBookingOngoing(self, bookingID, ongoing):
        with BookingDatabaseUtils() as db:
            db.setBookingOngoing(bookingID, ongoing)

    def setBookingDuration(self, bookingID, duration):
        with BookingDatabaseUtils() as db:
            db.setBookingDuration(bookingID, duration)

    def getLatestBookingID(self):
        with BookingDatabaseUtils() as db:
            for bookingID in db.getLatestBookingId():
                return int(bookingID[0])