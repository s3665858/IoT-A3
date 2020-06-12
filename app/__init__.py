from flask import Flask
from mainEngine import MainEngine
from server import SocketServer
from google_calendar.google_calendar_api import GoogleCalendarApi
from pushbullet.pushbullet_api import PushBulletAPI
from flask_googlemaps import GoogleMaps
from dynaconf import FlaskDynaconf

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
app.secret_key='abcd1234'

mainEngine = MainEngine()
gCalendar = GoogleCalendarApi()
pushBullet = PushBulletAPI()
gMap = GoogleMaps(app,key="AIzaSyCUg4PiYLKek3_gVcRiV-EWGRUH0vzqVMw")
dynaConf = FlaskDynaconf(app)

# Load the views
from app import views
# Load the config file
app.config.from_object('config')
