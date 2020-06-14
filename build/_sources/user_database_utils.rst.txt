.. _user_database_utils:

User Database Utils class
==========================
This class manages the *User* Table in our database *Data* by executing MySQL the appropriate queries.

Functions contained in this class:

__init__(self, connection = None)
---------------------------------------------
parameters: connection

function: If a connection is not established, establish a connection on MySQLdb with our private credentials.
::

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(CarDatabaseUtils.HOST, CarDatabaseUtils.USER,
                CarDatabaseUtils.PASSWORD, CarDatabaseUtils.DATABASE)
        self.connection = connection


close(self)
--------------
function: Closes the connection with the database.
::

    def close(self):
        self.connection.close()


__enter__(self)
----------------
function: Return the class itself.
::

    def __enter__(self):
        return self


__exit__(self, type, value, traceback)
------------------------------------------------
function: Executes close()
::

    def __exit__(self, type, value, traceback):
        self.close()


createUserTable(self)
-----------------------
function: Creates and initialises the User table
::

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


insertUser(self, name, password, firstname, lastname, email, acc_type)
----------------------------------------------------------------------------
parameters: *name*, *password*, *firstname*, *lastname*, *email*, *acc_type*

function: Inserts a user with the given parameters into the User table
::

    def insertUser(self, name, password, firstname, lastname, email, acc_type):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into User (username, password, firstname, lastname,email, type) values (%s, %s,%s, %s,%s, %s)", (name,password, firstname, lastname,email , acc_type,))
            
        self.connection.commit()

        return cursor.rowcount == 1


getUser(self)
-----------------
function: Query for the userID, username, password, firstname, lastname, email, type of all the rows 
in the User table
::

    def getUser(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select userID, username, password, firstname, lastname, email, type from User")
            return cursor.fetchall()


deleteUser(self, userID)
---------------------------
parameters: *UserID*

function: Deletes the row in the User table where the *userID* column has the same value to 
the parameter *UserID*.
::

    def deleteUser(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from User where userID = %s", (userID,))
        self.connection.commit()

updateUser(self, userID)
---------------------------
parameters: *UserID*
