import MySQLdb

class RepairDatabaseUtils:
    HOST = "35.244.89.13"
    USER = "root"
    PASSWORD = "1111"
    DATABASE = "Data"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(RepairDatabaseUtils.HOST, RepairDatabaseUtils.USER,
                RepairDatabaseUtils.PASSWORD, RepairDatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def createRepairTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Repairs (
                    repairID int not null auto_increment,
                    userID int not null,
                    CarID int not null,
                    ongoing int not null,
                    constraint PK_Repairs primary key (repairID)
                )""")
        self.connection.commit()

    def insertRepair(self, userID, CarID, status):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into Repairs (userID, CarID, ongoing) values (%s, %s, %s)", (userID, CarID, status,))
        self.connection.commit()

        return cursor.rowcount == 1

    def listPersonalRepairsHistory(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select repairID, CarID, ongoing from Repairs WHERE userID = %s", (userID,))
            return cursor.fetchall()

    def listPersonalOngoingRepairs(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select repairID, CarID, ongoing from Repairs WHERE userID = %s and ongoing = 1", (userID,))
            return cursor.fetchall()

    def setRepairStatus(self, bookingID, status):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE Repairs SET ongoing = %s where repairID = %s", (int(status), bookingID,))
        self.connection.commit()
    
    