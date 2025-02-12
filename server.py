import socket, pickle,json
from mainEngine import MainEngine
import face_recognition
import os
class SocketServer:
        
        
    def startListening(self):

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost' , 10000)
        self.serverSocket.bind(self.server_address)
        self.serverSocket.listen(5)
        while True:
            print('waiting for a connection')
            connection, client_address = self.serverSocket.accept()
            received = connection.recv(4096)
            if received:
                data = pickle.loads(received)
                if data['type']==1:
                    sendBack = pickle.dumps(self.validation(data))  
                    
                if data['type']==2:
                    sendBack = pickle.dumps(self.faceValidation(data))

                if data['type']==3:
                    sendBack = pickle.dumps(self.returnCar(data))

                if data['type']==4:
                    sendBack = pickle.dumps(self.engineerValidation(data))
                
                if data['type']==5:
                    sendBack = pickle.dumps(self.engineerSignIn(data))
            
            connection.sendall(sendBack)
            connection.close()

    def engineerValidation(self,data):
        mainEngine = MainEngine()
        alladdress = mainEngine.getAllAddress()
        for device in data['nearby_devices']:
            for address in alladdress:
                if(device == address[0]):
                    return True
        return  False

    def engineerSignIn(self,data):
        mainEngine = MainEngine()
        details = mainEngine.getAllDetails()
        for detail in details:
            if data['id'] == detail[1]:
                name = mainEngine.getUserDetails(detail[1])[0][1]
                if data['name']==name:
                    mainEngine.setCarAvailability(data['carID'],1)
                    repairs = mainEngine.listPersonalOngoingRepairs(data['id'])
                    for repair in repairs:
                        if data['carID']==repair[1]:
                            mainEngine.setRepairStatus(repair[0],0)
                            return True
        return False
    def validation(self,data):
        mainEngine = MainEngine()
        username = data['username']
        password = data['password']
        carId = data['carId']
       
        if mainEngine.login(username,password):
            userID = mainEngine.getUser(username)[0]
            ongoingbookings = mainEngine.listPersonalOngoingBooking(userID)
            for booking in ongoingbookings:
                if booking[1] == carId:
                    return userID
                    break
        return -1

    def createEncoding(self,known_image,userID):
        file = open('encodings.dat','wb+')
        encodings = {}
        if os.path.getsize('encodings.dat')>0:
            encodings = pickle.load(file)
        image = face_recognition.load_image_file(known_image)
        encodings[userID] = face_recognition.face_encodings(image)[0]
        pickle.dump(encodings,file,pickle.HIGHEST_PROTOCOL)

    def faceValidation(self,data):
        mainEngine = MainEngine()
        file = open('encodings.dat','rb')
        encodings = pickle.load(file)
        for index,encoding in encodings.items():
            results = face_recognition.compare_faces([encoding],data['encoding'])
            if results[0]:
                userID = index
                ongoingbookings = mainEngine.listPersonalOngoingBooking(userID)
                for booking in ongoingbookings:
                    if booking[1] == data['carid']:
                        return index

        return -1
    
    def returnCar(self,data):
        mainEngine = MainEngine()
        userID = data['userid']
        carID = data['carid']
        location = data['location']
        ongoingbookings = mainEngine.listPersonalOngoingBooking(userID)
        for booking in ongoingbookings:
            if booking[1] == carID:
                mainEngine.setBookingOngoing(booking[0],0)
                mainEngine.setCarAvailability(carID,1)
                mainEngine.setCarLocation(carID,location)
                return True
        return False
