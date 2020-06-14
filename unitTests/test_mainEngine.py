import unittest
from mainEngine import MainEngine

class MainEngineTest(unittest.TestCase):
    def setUp(self):
        self.mainEngine = MainEngine()
    
    def testHashSuccessful(self):
        hashed = self.mainEngine.hash_password("1234")
        self.assertTrue(self.mainEngine.verify_password(hashed,"1234"))
    
    def testHashFails(self):
        hashed = self.mainEngine.hash_password("1233")
        self.assertFalse(self.mainEngine.verify_password(hashed,"1234"))
        
    def testLoginSuccess(self):
        self.assertTrue(self.mainEngine.login("vincent","1234"))

    def testloginFails(self):
        self.assertFalse(self.mainEngine.login("vincent","1233"))
        
    def testRegisterFails(self):
        # self.assertTrue(self.mainEngine.check_duplicate_username("vincent"))
        self.assertTrue(self.mainEngine.check_isalnum_username("abc1234-="))
    
    def testRegisterSuccessful(self):
        # self.assertFalse(self.mainEngine.check_duplicate_username("iottest"))
        self.assertFalse(self.mainEngine.check_isalnum_username("abc1234"))
    
if __name__ == "__main__":
    unittest.main()
