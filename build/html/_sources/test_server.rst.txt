Unit Tests for Socket Server
================================
This class contains unit test functions for :ref:`socket_server`. Instead of running the queries 
on the actual database, we run them in *TestData* which is our database for unit testing.

Functions contained in this class:

setUp(self)
---------------
function: Initialises the all the classes needed for unit testing.
::

    def setUp(self):
        self.mainEngine = MainEngine()
        self.s = SocketServer()
        activate_job()
        self.mainEngine.insertBooking(3,1,2)


testValidation(self)
---------------------------
function: Tests the function *validation()* from :ref:`socket_server`. This is to test that the 
function would validate properly when given the correct user credentials who booked the specific car.
::

    def testValidation(self):
        
        data = {"type":1,"username":"rock","password":"1234","carId":1}
        self.assertTrue(self.s.validation(data))
        self.mainEngine.cancelBooking(self.mainEngine.getLatestBookingID())


testFaceValidate(self)
---------------------------
function: Tests the function *faceValidation()* from :ref:`socket_server`. This is to test that the 
function would validate properly when given the correct face image of the user who booked the specific car.
::

    def testFaceValidate(self):
        unknown_image = face_recognition.load_image_file("unknow.jpg")
        data = {"type":2,"encoding":face_recognition.face_encodings(unknown_image)[0],"carid":1}
        self.assertEqual(self.s.faceValidation(data),3)
        self.mainEngine.cancelBooking(self.mainEngine.getLatestBookingID())


testReturnCar(self)
---------------------------
function: Tests the function *returnCar()* from :ref:`socket_server`. This is to test that the 
function would be returned successfully with the correct data.
::

    def testReturnCar(self):
        location = ("Box Hill,-37.8214992,145.1086673")
        data = {'type':3,'carid':1,'userid':3,'location':location}
        self.assertTrue(self.s.returnCar(data))
