from flask import Flask, jsonify, render_template, request, redirect, session
from flask_googlemaps import Map
from flask_googlemaps import icons
from google_calendar.authenticator_runner import run_authenticator
from app import app, mainEngine, gCalendar, gMap, dynaConf
from werkzeug.utils import secure_filename
from server import SocketServer
@app.route('/')
def index():
    session.clear()
    return render_template("index.html")

@app.route('/register', methods = ('GET', 'POST'))
def registerPage():
    usernameDuplicate=False
    usernameInvalid=False
    registered=False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        if mainEngine.check_duplicate_username(username) is False and mainEngine.check_isalnum_username(username) is False:
            mainEngine.register(username, password, fname, lname, email)
            registered=True
        elif mainEngine.check_duplicate_username(username) is True:
            usernameDuplicate=True
        elif mainEngine.check_isalnum_username(username) is True:
            usernameInvalid=True
    return render_template("register.html", registered=registered, usernameDuplicate=usernameDuplicate , usernameInvalid=usernameInvalid)

@app.route('/login', methods = ('GET', 'POST'))
def loginPage():
    error=False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if mainEngine.login(username, password):
            user=mainEngine.getUser(username)
            session['userID']=user[0]
            session['username']=username
            session['type']=user[6]
            return redirect('/home')
        else:
            error=True 
    return render_template("login.html", error=error)

@app.route('/home')
def home():
    if session['type']=='c':
        return render_template("customer/home.html", name=session.get('username'))
    else:
        return render_template("admin/home.html", name=session.get('username'))

@app.route('/carlist', methods=["GET"])
def cars():   
    if session['type']=='c':
        mark=[]
        cars=mainEngine.listAvailableCars()
        for car in cars:
            print(car[5])
            x = car[5].split(",")
            mark.append((float(x[1]), float(x[2]), car[1]))
        gmap = Map(
            identifier="gmap",
            varname="gmap",
            #MELBOURNE COORDINATE
            lat=-37.8136,
            lng=144.9631,
            markers={
                icons.dots.blue: mark,
            },
            style="height:300px;width:300px;margin:0;margin-left:auto;margin-right:auto;",
        )
        return render_template("customer/carlist.html",cars=cars, gmap=gmap)
    else:
        mark=[]
        cars=mainEngine.listCars()
        for car in cars:
            x = car[5].split(",")
            mark.append((float(x[1]), float(x[2]), car[1]))
        gmap = Map(
            identifier="gmap",
            varname="gmap",
            #MELBOURNE COORDINATE
            lat=-37.8136,
            lng=144.9631,
            markers={
                icons.dots.blue: mark,
            },
            style="height:300px;width:300px;margin:0;margin-left:auto;margin-right:auto;",
        )
        return render_template("admin/carlist.html",cars=cars, gmap=gmap)

@app.route('/addcar', methods = ('GET', 'POST'))
def addcar():
    if request.method == 'POST':
        name = request.form['name']
        bodytype = request.form['bodytype']
        colour = request.form['colour']
        seats = request.form['seats']
        location = request.form['location']
        cost = request.form['cost']
        mainEngine.insertCar(name, bodytype, colour, seats, location, cost)
        return redirect('/carlist')
    else:
        return render_template("admin/addcar.html")

@app.route('/set_car_availability_to_unavailable', methods = ['POST'])
def set_car_availability_to_unavailable():
    carID = request.form['switch_to_unavailable']
    mainEngine.setCarAvailability(carID, 0)
    return redirect('/carlist')

@app.route('/set_car_availability_to_available', methods = ['POST'])
def set_car_availability_to_available():
    carID = request.form['switch_to_available']
    mainEngine.setCarAvailability(carID, 1)
    return redirect('/carlist')

@app.route('/deletecar', methods = ['POST'])
def deletecar():
    carID = request.form['delete']
    mainEngine.deleteCar(carID)
    return redirect('/carlist')

@app.route('/userlist', methods=["GET"])
def users():
    users=mainEngine.listUsers()
    return render_template("admin/userlist.html",users=users)

@app.route('/deleteuser', methods = ['POST'])
def deleteuser():
    userID = request.form['delete']
    mainEngine.deleteUser(userID)
    return redirect('/userlist')

@app.route('/searchcar', methods = ('GET', 'POST'))
def searchcar():
    cars={}
    search=""
    column=""
    if request.method == 'POST':
        column = request.form['column']
        search = request.form['search']        
        cars=mainEngine.searchCars(column, search)
    return render_template("customer/searchcar.html", search=search, column=column, cars=cars)

@app.route('/bookhistory')
def history():
    bookings = mainEngine.listPersonalBookingHistory(session['userID'])
    cars=mainEngine.listCars()
    return render_template("customer/bookhistory.html", cars=cars, bookings=bookings)

@app.route('/makebooking', methods = ['POST'])
def makebooking():
    carID = request.form['car']
    make = request.form['make']
    location = request.form['location']
    duration = request.form['duration']
    bookingID = int(mainEngine.getLatestBookingID())+1
    valid = gCalendar.insert_booking(str(bookingID), session['userID'], make, location, duration)
    if valid is False:
        return redirect('/googleAuthenticate')
    else:
        mainEngine.insertBooking(session['userID'], carID, duration)
        mainEngine.setCarAvailability(carID, 0)
    return redirect('/booking')    

@app.route('/uploader',  methods = ['POST'])
def upload_file():
    userID = session['userID']
    print(session['userID'])
    f = request.files['file']
    s = SocketServer()
    s.createEncoding(f,userID)
    return redirect('/home')

@app.route('/booking')
def booking():
	bookings = mainEngine.listPersonalOngoingBooking(session['userID'])
	cars=mainEngine.listCars()
	return render_template("customer/booking.html", cars=cars, bookings=bookings)

@app.route('/deletebooking', methods = ['POST'])
def deletebooking():
    bookingID = request.form['delete']
    userID = session['userID']
    make = request.form['make']
    # location = request.form['location']
    # duration = request.form['duration']
    bookings = mainEngine.listPersonalOngoingBooking(userID)
    carID = ""
    for booking in bookings:
        if booking[0]==int(bookingID):
            carID = booking[1]
    mainEngine.setCarAvailability(carID, 1)
    mainEngine.setBookingOngoing(bookingID, 2)
    gCalendar.delete_booking(bookingID, userID, make)
    return redirect('/booking')

@app.route('/googleAuthenticate', methods = ('GET', ('POST')))
def googleAuthenticate():
    if request.method == 'POST':
        code = request.form['code']
        userID = session['userID']
        run_authenticator(userID,code)
        return redirect("/googleAuthenticationComplete")
    else:
        return render_template("customer/googleAuthentication.html")

@app.route('/googleAuthenticationComplete')
def googleAuthenticationComplete():
    return render_template("customer/googleAuthenticationComplete.html")


