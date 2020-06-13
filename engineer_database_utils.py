import MySQLdb

class EngineerDatabaseUtils:
    HOST = "35.244.89.13"
    USER = "root"
    PASSWORD = "1111"
    DATABASE = "Data"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(EngineerDatabaseUtils.HOST, EngineerDatabaseUtils.USER,
                EngineerDatabaseUtils.PASSWORD, EngineerDatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def createEngineerTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Engineers (
                    engineerID int not null auto_increment,
                    userID int not null,
                    address text not null,
                    constraint PK_Engineers primary key (engineerID)
                )""")
        self.connection.commit()

    def insertEngineer(self, userID, address):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into Engineers (userID, address) values (%s, %s)", (userID, address,))
        self.connection.commit()

        return cursor.rowcount == 1

    def deleteAddress(self, address):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from Engineers where engineerID = %s", (address,))
        self.connection.commit()

        return cursor.rowcount == 1

    def listAllEngineers(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Engineers")
            return cursor.fetchall()
        
    def getEngineerAddress(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Engineers WHERE userID = %s", (userID,))
            return cursor.fetchall()

    def getEngineerUserID(self, address):
        with self.connection.cursor() as cursor:
            cursor.execute("select userID from Engineers WHERE address = %s", (address,))
            return cursor.fetchall()
    
    def getAllAddress(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select address from Engineers")
            return cursor.fetchall()
    
    def getAllDetails(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Engineers")
            return cursor.fetchall()