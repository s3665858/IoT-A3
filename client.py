import socket, pickle
import face_recognition
import bluetooth
from os import path
import threading
from pyzbar.pyzbar import decode
from PIL import Image
import ast
class SocketClient:

    carID = -1
    userID = -1
    
    def __init__(self):
        if path.exists("data.dat"):
            file = open("data.dat","rb")
            info = pickle.load(file)
            self.carID = info[0]
            self.userID = info[1]
        
    def setUserID(self, id):
        self.userID = id

    def setCarID(self,id):
        self.carID = id

    def sendData(self,data):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 10000)
        self.sock.connect(self.server_address)
        self.sock.sendall(data)
        received = self.sock.recv(4096)
        data = pickle.loads(received)
        self.sock.close()
        return data

    def unlockCar(self):
        username = input("please input your user name:\n")
        password = input("please input your password:\n")
        account = {"type":1,"username":username,"password":password,"carId":self.carID}
        data = pickle.dumps(account)
        self.userID = self.sendData(data)
        if self.userID > -1:
            print("unlock")
            
        else:
            print("your face is not in database or you did not book this car")

    
    def faceunlock(self):
        unknown_image = face_recognition.load_image_file("unknow.jpg")
        data = {"type":2,"encoding":face_recognition.face_encodings(unknown_image)[0],"carid":self.carID}
        data = pickle.dumps(data)
        self.userID = self.sendData(data)
        print(self.userID)
        if self.userID > -1:
            print("unlock")
            
        else:
            print("invalid username and password or u did not book thiscar")

    def returnCar(self):
        location = ("Box Hill,-37.8214992,145.1086673")
        data = {'type':3,'carid':self.carID,'userid':self.userID,'location':location}
        data = pickle.dumps(data)
        if self.sendData(data):
            print("return successfully")
        else:
            print("this car is not being rented")

    def engineerUnlock(self,nearby_devices):
        data = {'type':4,'carid':self.carID,'nearby_devices':nearby_devices}
        data = pickle.dumps(data)
        if self.sendData(data):
            print("unlock")
            return True
        
    

    def saveData(self):
        file = (open("data.dat","wb"))
        info = [self.carID,self.userID]
        pickle.dump(info,file)
        
    def menu(self):
        
        menu = True
        while True:
            print("1.unlock car with username and password\n")
            print("2.unlock car with face recognition\n")
            print("3.return the car\n")
            print('4.engineer sign in')
            menu = input()

            if menu == '1':
                
                self.unlockCar()
                self.saveData()
                
                break
                
            
            if menu == '2':
                self.faceunlock()
                self.saveData()
                break

            if menu =="3":
                self.returnCar()
                self.saveData()
                break
            if menu =="4":
                self.engineerSignin('1.jpg')
                break
            else:
                print("invalid input")

    def detectBluetoothDevices(self):
        count = 0
        while count<5:
            nearby_devices = bluetooth.discover_devices()
            count +=1
            if(self.engineerUnlock(nearby_devices)):
                break

    
    def engineerSignin(self,file):
        data = ast.literal_eval(decode(Image.open(file))[0].data.decode('UTF-8'))
        data['carID'] = self.carID
        dataToSend = pickle.dumps(data)
        if self.sendData(dataToSend):
            print('success')
        else:
            print("invalid QR code or car no need to repair")
        
    


#new thread for detecting nearby bluetooth devices
def activate_job():
    def run_job():
        s.detectBluetoothDevices()
    thread = threading.Thread(target=run_job)
    thread.start()


s = SocketClient()
activate_job()
s.setCarID(5)
s.menu()



