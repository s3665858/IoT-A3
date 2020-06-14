# Reference: https://docs.python.org/2/library/unittest.html
import unittest
import MySQLdb
from engineer_database_utils import EngineerDatabaseUtils

class TestDatabaseUtils(unittest.TestCase):
    HOST = "34.87.224.11"
    USER = "root"
    PASSWORD = "1111"
    DATABASE = "TestData"

    def setUp(self):
        self.connection = MySQLdb.connect(TestDatabaseUtils.HOST, TestDatabaseUtils.USER,
            TestDatabaseUtils.PASSWORD, TestDatabaseUtils.DATABASE)
        
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists Engineers")
            cursor.execute("""
                create table if not exists Engineers (
                    engineerID int not null auto_increment,
                    userID int not null,
                    address text not null,
                    constraint PK_Engineers primary key (engineerID)
                )""")
            cursor.execute("insert into Engineers (userID, address) values (1, 00:0a:95:9d:68:16)")
        self.connection.commit()

    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countEngineers(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Engineers")
            return cursor.fetchone()[0]

    def countEngineersByID(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Engineers where userID = %s", (userID,))
            return cursor.fetchone()[0]

    def test_insertEngineer(self):
        with EngineerDatabaseUtils(self.connection) as db:
            count = self.countEngineers()
            self.assertTrue(db.insertEngineer(2, '00:0a:95:9d:68:16'))
            self.assertTrue(count + 1 == self.countEngineers())
            self.assertTrue(db.insertEngineer(3, '00:0a:95:9d:68:17'))
            self.assertTrue(count + 1 == self.countEngineers())

    def test_listAllEngineers(self):
        with EngineerDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countEngineers() == len(db.listAllEngineers()))

    def test_deleteAddress(self):
        with EngineerDatabaseUtils(self.connection) as db:
            count = self.countEngineers()
            userID = 1

            self.assertTrue(self.countEngineersByID(userID))

            db.deleteAddress(userID)

            self.assertFalse(self.countEngineersByID(userID))
            self.assertTrue(count - 1 == self.countEngineers())

    def test_getEngineerUserID(self):
        with EngineerDatabaseUtils(self.connection) as db:
            userID = 4
            address = '00:0a:95:9d:68:26'
            db.insertEngineer(userID, address)
            self.assertTrue(userID == db.getEngineerUserID(address))

    def test_getAllAddress(self):
        with EngineerDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countEngineers() == len(db.getAllAddress()))

    def test_getAllDetails(self):
        with EngineerDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countEngineers() == len(db.getAllDetails()))

if __name__ == "__main__":
    unittest.main()

