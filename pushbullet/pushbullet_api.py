from pushbullet import Pushbullet

class PushBulletAPI:
    
    def __init__(self):
        self.pb = Pushbullet('o.BfDh4Z35MEnCyxal5J0dcIuMamGyU38a')

    def pushNotification(self, carID, car_make):
        push = self.pb.push_note("Car require repair", "Car ID: "+carID+" ,Car Make: "+car_make)
        

