from pushbullet import Pushbullet

class PushBulletAPI:
    
    def main(self):
        self.pushNotification(10, "Toyota")

    def __init__(self):
        self.pb = Pushbullet('o.BfDh4Z35MEnCyxal5J0dcIuMamGyU38a')

    def pushNotification(self, carID, car_make):
        push = self.pb.push_note("Car require repair", "Car ID: "+str(carID)+" ,Car Make: "+car_make)
        
PushBulletAPI().main()