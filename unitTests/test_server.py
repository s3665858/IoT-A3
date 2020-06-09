from server import SocketServer
from mainEngine import MainEngine
import unittest
import pickle
import face_recognition
def activate_job():
    def run_job():
        socket = SocketServer()
        socket.startListening()




class MainEngineTest(unittest.TestCase):
    def setUp(self):
        self.mainEngine = MainEngine()
        self.s = SocketServer()
        activate_job()
        self.mainEngine.insertBooking(3,1,2)
    def testValidation(self):
        
        data = {"type":1,"username":"rock","password":"1234","carId":1}
        self.assertTrue(self.s.validation(data))
        self.mainEngine.cancelBooking(self.mainEngine.getLatestBookingID())
        
    
    def testFaceValidate(self):
        unknown_image = face_recognition.load_image_file("unknow.jpg")
        data = {"type":2,"encoding":face_recognition.face_encodings(unknown_image)[0],"carid":1}
        self.assertEqual(self.s.faceValidation(data),3)
        self.mainEngine.cancelBooking(self.mainEngine.getLatestBookingID())
   
    def testReturnCar(self):
        location = ("Box Hill,-37.8214992,145.1086673")
        data = {'type':3,'carid':1,'userid':3,'location':location}
        self.assertTrue(self.s.returnCar(data))


if __name__ == "__main__":
    unittest.main()