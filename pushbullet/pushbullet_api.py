from pushbullet import Pushbullet

class PushBulletAPI:
    
    def main(self):
        self.pb = Pushbullet('o.v2SWZxf3qJCmQSqHDLeYdElsnPf0EqVp')

    def sendEmail(self, name, email, carID, car_make):
        recipient = self.pb.new_contact(name, email)
        push = self.pb.push_note("Dear "+name+", we are sending over a car for repairs. CarID: "+carID+" Car make: "+ car_make, contact=recipient)
       
PushBulletAPI().main()
