import MySQLdb

class UserDatabaseUtils:
    # changed the host and database and functions
    HOST = "35.244.89.13"
    USER = "root"
    PASSWORD = "1111"
    DATABASE = "Data"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(UserDatabaseUtils.HOST, UserDatabaseUtils.USER,
                UserDatabaseUtils.PASSWORD, UserDatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def createUserTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists User (
                    userID int not null auto_increment,
                    firstname text not null,
                    lastname text not null,
                    email text not null,
                    username text not null,
                    password text not null,
                    type text not null,
                    constraint PK_User primary key (userID)
                )""")
        self.connection.commit()

    def insertUser(self, name, password, firstname, lastname, email, acc_type):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into User (username, password, firstname, lastname,email, type) values (%s, %s,%s, %s,%s, %s)", (name,password, firstname, lastname,email , acc_type,))
            
        self.connection.commit()

        return cursor.rowcount == 1
    
    def getUser(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select userID, username, password, firstname, lastname, email, type from User")
            return cursor.fetchall()
    
    def getUserDetails(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select userID, username, password, firstname, lastname, email, type from User WHERE userID = %s" , (userID,))
            return cursor.fetchall()

    def searchUsersbyUsername(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select userID, username, password, firstname, lastname, email, type from User WHERE lower(username) like %s", ('%' +search + '%',))
            return cursor.fetchall()

    def searchUsersbyFirstName(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select userID, username, password, firstname, lastname, email, type from User WHERE lower(firstname) like %s", ('%' +search + '%',))
            return cursor.fetchall()

    def searchUsersbyLastName(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select userID, username, password, firstname, lastname, email, type from User WHERE lower(lastname) like %s", ('%' +search + '%',))
            return cursor.fetchall()
        
    def searchUsersbyEmail(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select userID, username, password, firstname, lastname, email, type from User WHERE lower(email) like %s", ('%' +search + '%',))
            return cursor.fetchall()

    def searchUsersbyType(self, search):
        with self.connection.cursor() as cursor:
            cursor.execute("select userID, username, password, firstname, lastname, email, type from User WHERE type = %s", (search,))
            return cursor.fetchall()

    def deleteUser(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from User where userID = %s", (userID,))
        self.connection.commit()