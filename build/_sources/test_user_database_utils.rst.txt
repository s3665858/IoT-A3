Unit Tests for User Database Utils
=========================================
This class contains unit test functions for :ref:`user_database_utils`. Instead of running the queries 
on the actual databse, we run them in *TestData* which is our database for unit testing.

Functions contained in this class:

setUp(self)
---------------
function: Creates the User Table in our *TestData* database.
::

    def setUp(self):
        self.connection = MySQLdb.connect(TestDatabaseUtils.HOST, TestDatabaseUtils.USER,
            TestDatabaseUtils.PASSWORD, TestDatabaseUtils.DATABASE)
        
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists User")
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
            cursor.execute("insert into User (firstname, lastname, email, username, password, type) values ('Vincent','Pranata','abcd@gmail.com','s3665858','abcd','a')")
            cursor.execute("insert into User (firstname, lastname, email, username, password, type) values ('Guoxin','Shan','1234@gmail.com','rock','1234','c')")
            cursor.execute("insert into User (firstname, lastname, email, username, password, type) values ('Sean','Tan','test@gmail.com','test','1111','c')")
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


countUser(self)
------------------
function: Counts the number of users in the database for testing the functions.
::

    def countUser(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from User")
            return cursor.fetchone()[0]


userExists(self, userID)
---------------------------
parameters: *userID*

function: Checks if the user with the *userID* parameter given exist in the table.
::

    def userExists(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from User where userID = %s", (userID,))
            return cursor.fetchone()[0] == 1


test_insertUser(self)
-----------------------
function: Tests the function *insertUser()* from :ref:`user_database_utils`. First it counts the number 
of users with *countUser()*, then adds some users into the database and then make sure the counts increases accordingly.
::

    def test_insertUser(self):
        with UserDatabaseUtils(self.connection) as db:
            count = self.countUser()
            self.assertTrue(db.insertUser('Vincent','Pranata','abcd@gmail.com',"s3665858",'abcd','a'))
            self.assertTrue(count + 1 == self.countUser())
            self.assertTrue(db.insertUser('Sean','Tan','abcd@gmail.com','test','1111','a'))
            self.assertTrue(count + 2 == self.countUser())


test_getUser(self)
-----------------------
function: Tests the function *getUser()* from :ref:`user_database_utils`. The test is made by comparing 
the number obtained from *countUser()* with it.
::

    def test_getUser(self):
        with UserDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countUser() == len(db.getUser()))


test_deleteUser(self)
-----------------------
function: Tests the function *deleteUser()* from :ref:`user_database_utils`. First it counts the number 
of users with *countUser()*, then deletes a user from the database and then make sure the count decreases by 1.
::

    def test_deleteUser(self):
        with UserDatabaseUtils(self.connection) as db:
            count = self.countUser()
            userID = 1

            self.assertTrue(self.userExists(userID))

            db.deleteUser(userID)

            self.assertFalse(self.userExists(userID))
            self.assertTrue(count - 1 == self.countUser())




