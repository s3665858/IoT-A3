Unit Tests for Main Engine
================================
This class contains unit test functions for :ref:`main_engine`. Instead of running the queries 
on the actual database, we run them in *TestData* which is our database for unit testing.

Functions contained in this class:

setUp(self)
---------------
function: Initialises the Main Engine object.
::

    def setUp(self):
        self.mainEngine = MainEngine()


testHashSuccessful(self)
---------------------------
function: Tests the function *hash_password()* and *verify_password()* from :ref:`main_engine`. This is to test that the 
function would hash the password and verified successfully and correctly.
::

    def testHashSuccessful(self):
        hashed = self.mainEngine.hash_password("1234")
        self.assertTrue(self.mainEngine.verify_password(hashed,"1234"))


testHashFails(self)
-------------------------
function: Tests the function *hash_password()* and *verify_password()* from :ref:`main_engine`. This is to test that the 
function would hash the password successfully but comparing it with a wrong value. The verification is 
expected to fail.
::

    def testHashFails(self):
        hashed = self.mainEngine.hash_password("1233")
        self.assertFalse(self.mainEngine.verify_password(hashed,"1234"))


testLoginSuccess(self)
-------------------------
function: Tests the function *login()* from :ref:`main_engine`. This is to test that the 
function would have a successful login when a valid username and password is entered.
::

    def testLoginSuccess(self):
        self.assertTrue(self.mainEngine.login("vincent","1234"))


testloginFails(self)
-------------------------
function: Tests the function *login()* from :ref:`main_engine`. This is to test that the 
function would have a failed login when an invalid username and password is entered.
::

    def testloginFails(self):
        self.assertFalse(self.mainEngine.login("vincent","1233"))


testRegisterFails(self)
-----------------------------
function: Tests the function *check_duplicate_username()* *check_isalnum_username* in the *register()* function 
from :ref:`main_engine`. This is to test that the function would have a failed registration when given 
either a duplicate username or a username which is not alphanumeric.
::

    def testRegisterFails(self):
        self.assertTrue(self.mainEngine.check_duplicate_username("vincent"))
        self.assertTrue(self.mainEngine.check_isalnum_username("abc1234-="))


testRegisterSuccessful(self)
-----------------------------
function: Tests the function *check_duplicate_username()* *check_isalnum_username* in the *register()* function 
from :ref:`main_engine`. This is to test that the function would have a successful registration when given 
a non-duplicate username and a username which is alphanumeric.
::

    def testRegisterSuccessful(self):
        self.assertFalse(self.mainEngine.check_duplicate_username("iottest"))
        self.assertFalse(self.mainEngine.check_isalnum_username("abc1234"))
