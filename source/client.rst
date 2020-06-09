.. _client:

Socket Client class
=====================
*Directory: /client.py*

This class acts as a console interface for the customer on AP. It helps with user validation to unlock the 
car and also returning the car. All information received from AP is sent to the :ref:`socket_server` 
in MP via sockets.

Functions contained in this class:

menu(self)
------------------
function: The main() function of this class. Gives the user the option to unlock the car with a username 
and password or usig face recognition. The user can also return the car using this function. The main() 
function will call the appropriate functions within this class depending on the user's actions.
::

    def menu(self):
        
        menu = True
        while True:
            print("1.unlock car with username and password\n")
            print("2.unlock car with face recognition\n")
            print("3.return the car")
            menu = input()

            if menu == '1':
                if self.unlockCar():
                    print("unlock")
                else:
                    print("invalid username and password or u did not book thiscar")
                break
            
            if menu == '2':
                self.faceunlock()
                break

            if menu =="3":
                self.returnCar()
                break
            else:
                print("invalid input")


__init__(self)
------------------
function: Does something.....
::

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 10000)
        self.sock.connect(self.server_address)


setUserID(self, id)
---------------------
parameters: *id*

function: Set the *userID* of this class to the parameter *id*.
::

    def setUserID(self, id):
        self.userID = id


setCarID(self,id)
--------------------
parameters: *id*

function: Set the *carID* of this class to the parameter *id*.
::

    def setCarID(self,id):
        self.carID = id


sendData(self,data)
--------------------
parameters: *data*

function: Sends the *data* parameter received to the MP and gets a response back via the :ref:`socket_server`.
::

    def sendData(self,data):
        self.sock.sendall(data)
        received = self.sock.recv(4096)
        data = pickle.loads(received)
        self.sock.close()
        return data


unlockCar(self)
-------------------
function: Takes in the *username* and *password* from the user through the console input. It then packages 
the *username*, *password* and *carID* into a data package and sends it to the *validation()* function 
in :ref:`socket_server` from MP via the *sendData()* function in this class. 
If a success response is received, the car will be unlocked.
::

    def unlockCar(self):
        username = input("please input your user name:\n")
        password = input("please input your password:\n")
        account = {"type":1,"username":username,"password":password,"carId":self.carID}
        data = pickle.dumps(account)
        return self.sendData(data)


returnCar(self)
--------------------
function: Packages the *location* of the car into a data package and sends it to the *validation()* 
function in :ref:`socket_server` from MP via the *sendData()* function in this class. 
If the response received is True , the car will be successfully returned.
::

    def returnCar(self):
        location = ("Box Hill,-37.8214992,145.1086673")
        data = {'type':3,'carid':self.carID,'userid':self.userID,'location':location}
        data = pickle.dumps(data)
        if self.sendData(data):
            print("return successfully")
        else:
            print("this car is not being rented")


faceunlock(self)
--------------------
function: Packages the facial recognition encodings into a data package and sends it to the *faceValidation()* 
function from MP via the *sendData()* function. If the userID returned matches the userID who booked 
the car, the car unlocks.
::

    def faceunlock(self):
        unknown_image = face_recognition.load_image_file("unknown.jpg")
        data = {"type":2,"encoding":face_recognition.face_encodings(unknown_image)[0],"carid":self.carID}
        data = pickle.dumps(data)
        self.userID = self.sendData(data)
        if self.userID > -1:
            print("unlock")
            
        else:
            print("your face is not in database or you did not book this car")



