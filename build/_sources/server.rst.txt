.. _socket_server:

Socket Server class
======================
*Directory: /server.py*

The Socket Server class is location on MP and manages all information received from the 
:ref:`client` in AP via sockets. The information is processed accordingly and sent back again to the 
:ref:`client` in AP via sockets.

Functions contained in this class:

startListening(self)
----------------------
function: Allows the socket server to listen to the :ref:`client` when the user interacts 
with its console UI.
::

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
            
            connection.sendall(sendBack)
            connection.close()


validation(self,data)
----------------------
parameters: *data*

function: Receives username and password from the client through the :ref:`client` from the *data* parameter. 
It then calls the *login()* function from :ref:`main_engine` to validate the user, then it calls 
*listPersonalOngoingBooking()* from :ref:`main_engine` to validate that this user has made a booking 
with this specific car.
::

    def validation(self,data):
        mainEngine = MainEngine()
        username = data['username']
        password = data['password']
        carId = data['carId']
        isVaild = False
        if mainEngine.login(username,password):
            userID = mainEngine.getUser(username)[0]
            ongoingbookings = mainEngine.listPersonalOngoingBooking(userID)
            for booking in ongoingbookings:
                if booking[1] == carId:
                    isVaild = True
                    break
        return isVaild


createEncoding(self,known_image,userID)
-------------------------------------------
parameters: *known_image*, *userID*

function: Creates a facial recognition encoding with the image given from the *known_image* parameter 
and saves this encoding under the *userID* parameter given. 

::

    def createEncoding(self,known_image,userID):
        file = open('encodings.dat','wb+')
        encodings = {}
        if os.path.getsize('encodings.dat')>0:
            encodings = pickle.load(file)
        image = face_recognition.load_image_file(known_image)
        encodings[userID] = face_recognition.face_encodings(image)[0]
        pickle.dump(encodings,file,pickle.HIGHEST_PROTOCOL)


faceValidation(self,data)
------------------------------
parameters: *data*

function: Compares the facial recognition encoding provided in the *data* parameter and compares it 
with all the facial recognition encodings stored in the server. If a matching userID is found, compares 
it with the userID who booked the car.
::

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


returnCar(self,data)
----------------------
parameters: *data*

function: Receives the *userID*, *carID* and *location* of the returned car using the *data* parameter given.

Completes the booking by: 
* Calling *setBookingOngoing(booking[0],0)* from :ref:`main_engine` to set the booking as no longer ongoing.
* Calling *setCarAvailability(carID,1)* from :ref:`main_engine` to set the car to available for booking.
* Calling *setCarLocation(carID,location)* from :ref:`main_engine` to set the car location to its current location.
::

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


