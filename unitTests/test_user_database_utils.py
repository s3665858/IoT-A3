# Reference: https://docs.python.org/2/library/unittest.html
import unittest
import MySQLdb
from user_database_utils import UserDatabaseUtils

class TestDatabaseUtils(unittest.TestCase):
    HOST = "34.87.224.11"
    USER = "root"
    PASSWORD = "1111"
    DATABASE = "TestData"

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

    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countUser(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from User")
            return cursor.fetchone()[0]

    def userExists(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from User where userID = %s", (userID,))
            return cursor.fetchone()[0] == 1

    def test_insertUser(self):
        with UserDatabaseUtils(self.connection) as db:
            count = self.countUser()
            self.assertTrue(db.insertUser('Vincent','Pranata','abcd@gmail.com',"s3665858",'abcd','a'))
            self.assertTrue(count + 1 == self.countUser())
            self.assertTrue(db.insertUser('Sean','Tan','abcd@gmail.com','test','1111','a'))
            self.assertTrue(count + 2 == self.countUser())

    def test_getUser(self):
        with UserDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countUser() == len(db.getUser()))

    def test_deleteUser(self):
        with UserDatabaseUtils(self.connection) as db:
            count = self.countUser()
            userID = 1

            self.assertTrue(self.userExists(userID))

            db.deleteUser(userID)

            self.assertFalse(self.userExists(userID))
            self.assertTrue(count - 1 == self.countUser())

if __name__ == "__main__":
    unittest.main()

