import hashlib, binascii, os
from user_database_utils import UserDatabaseUtils
from car_database_utils import CarDatabaseUtils
from booking_database_utils import BookingDatabaseUtils
from engineer_database_utils import EngineerDatabaseUtils
from repair_database_utils import RepairDatabaseUtils

class MainEngine:
    def __init__(self):
        self.createUserTable()
        self.createCarTable()
        self.createBookingTable()
        self.createEnginnerTable()
        self.createRepairTable()
        
    def createUserTable(self):
        with UserDatabaseUtils() as db:
            db.createUserTable()
    
    def getUser(self, username):
        with UserDatabaseUtils() as db:
            for user in db.getUser():
                if user[1]==username:
                    return user
                
    def getOtherUser(self, userID):
        with UserDatabaseUtils() as db:
            return db.getOtherUser(userID)
    
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

    def update_check_duplicate_username(self, userID, username):
        users=self.getOtherUser(userID)
        for user in users:
            if user[1]==username:
                 return True
        return False

    # return False if no duplicates
    def check_duplicate_username(self, userID, username):
        user=self.getUser(userID)
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

    def getUserDetails(self, userID):
        with UserDatabaseUtils() as db:
            return db.getUserDetails(int(userID))

    def updateUser(self, userID, name, password, fname, lname, email, acc_type):
        with UserDatabaseUtils() as db:
            db.updateUser(userID, name, self.hash_password(password), fname, lname, email, acc_type)

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
            
    #user input to be transferred to ManagerView and CustomerView
    def listCars(self):
        with CarDatabaseUtils() as db:
            return db.listCars()
        
    def listAvailableCars(self):
        with CarDatabaseUtils() as db:
            return db.listAvailableCars()

    def listBrokenCars(self):
        with CarDatabaseUtils() as db:
            return db.listBrokenCars()

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

    ### functions for managing engineer table ###
    def createEnginnerTable(self):
        with EngineerDatabaseUtils() as db:
            db.createEngineerTable()
        
    def listEngineers(self):
        with EngineerDatabaseUtils() as db:
            return db.listAllEngineers()

    def insertEngineer(self, userID, address):
        with EngineerDatabaseUtils() as db:
            db.insertEngineer(userID, address)

    def deleteAddress(self, address):
        with EngineerDatabaseUtils() as db:
            db.deleteAddress(address)

    def getEngineerAddress(self, userID):
        with EngineerDatabaseUtils() as db:
            return db.getEngineerAddress(userID)

    def getAllAddress(self):
        with EngineerDatabaseUtils() as db:
            return db.getAllAddress()
    
    def getAllDetails(self):
        with EngineerDatabaseUtils() as db:
            return db.getAllDetails()
    
    def getEngineerUserID(self, address):
        with EngineerDatabaseUtils() as db:
            return db.getEngineerUserID(address)

    def getDurationForGraph(self):
        with BookingDatabaseUtils() as db:
            return db.getTop10Duration()

    def getTop10Make(self):
        with BookingDatabaseUtils() as db:
            return db.getTop10CarID()

    def getTop10BookingCountForMake(self):
        with BookingDatabaseUtils() as db:
            return db.getTop10CarIDCount()
    
    def getTop10Price(self):
        with CarDatabaseUtils() as db:
            return db.getTop10Price()

    def getTop10BookingCountForPrice(self):
        with BookingDatabaseUtils() as db:
            return db.getTop10PriceCount()

    def getTop10DurationCount(self):
        with BookingDatabaseUtils() as db:
            return db.getTop10DurationCount()

    ## functions for repair table ##
    def createRepairTable(self):
        with RepairDatabaseUtils() as db:
            db.createRepairTable()

    def insertRepair(self, userID, CarID):
        with RepairDatabaseUtils() as db:
            db.insertRepair(userID, CarID, 1)

    def listPersonalRepairsHistory(self, userID):
        with RepairDatabaseUtils() as db:
            return db.listPersonalRepairsHistory(userID)
            
    def listPersonalOngoingRepairs(self, userID):
        with RepairDatabaseUtils() as db:
            return db.listPersonalOngoingRepairs(userID)
    
    def cancelRepair(self, repairID):
        with RepairDatabaseUtils() as db:
            db.setRepairStatus(repairID, 2)

    def setRepairStatus(self, repairID, status):
        with RepairDatabaseUtils() as db:
            db.setRepairStatus(repairID, status)