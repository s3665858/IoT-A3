# Reference: https://docs.python.org/2/library/unittest.html
import unittest
import MySQLdb
from repair_database_utils import RepairDatabaseUtils

class TestDatabaseUtils(unittest.TestCase):
    HOST = "34.87.224.11"
    USER = "root"
    PASSWORD = "1111"
    DATABASE = "TestData"

    def setUp(self):
        self.connection = MySQLdb.connect(TestDatabaseUtils.HOST, TestDatabaseUtils.USER,
            TestDatabaseUtils.PASSWORD, TestDatabaseUtils.DATABASE)
        
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists Repairs")
            cursor.execute("""
                create table if not exists Repairs (
                    repairID int not null auto_increment,
                    userID int not null,
                    CarID int not null,
                    ongoing int not null,
                    constraint PK_Repairs primary key (repairID)
                )""")
            cursor.execute("insert into Repairs (userID, CarID, ongoing) values (1, 1, 0)")
            cursor.execute("insert into Repairs (userID, CarID, ongoing) values (2, 2, 0)")
        self.connection.commit()

    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countRepairs(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Repairs")
            return cursor.fetchone()[0]

    def countRepairsByID(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Repairs where userID = %s", (userID,))
            return cursor.fetchone()[0]

    def countOngoingRepairsByID(self, userID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Repairs where userID = %s and ongoing = 1", (userID,))
            return cursor.fetchone()[0]

    def repairExists(self, bookingID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Repairs where repairID = %s", (bookingID,))
            return cursor.fetchone()[0] == 1

    def repairIsOngoing(self, bookingID):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Repairs where repairID = %s and ongoing = 1", (bookingID,))
            return cursor.fetchone()[0] == 1    

    def test_insertRepairs(self):
        with RepairDatabaseUtils(self.connection) as db:
            count = self.countRepairs()
            self.assertTrue(db.insertRepair(3, 3, 1))
            self.assertTrue(count + 1 == self.countRepairs())
            self.assertTrue(db.insertRepair(4, 4, 1))
            self.assertTrue(count + 2 == self.countRepairs())

    def test_listPersonalRepairsHistory(self):
        userID = 1
        with RepairDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countRepairsByID(userID) == len(db.listPersonalRepairsHistory(userID)))

    def test_listPersonalOngoingRepairs(self):
        userID = 1
        with RepairDatabaseUtils(self.connection) as db:
            self.assertTrue(self.countOngoingRepairsByID(userID) == len(db.listPersonalOngoingRepairs(userID)))

    def test_setRepairStatus(self):
        with RepairDatabaseUtils(self.connection) as db:
            repairID = 1

            self.assertTrue(self.repairExists(repairID))
            self.assertFalse(self.repairIsOngoing(repairID))

            db.setRepairStatus(repairID, 1)

            self.assertTrue(self.repairIsOngoing(repairID))

            db.setRepairStatus(repairID, 0)

            self.assertFalse(self.repairIsOngoing(repairID))

if __name__ == "__main__":
    unittest.main()
