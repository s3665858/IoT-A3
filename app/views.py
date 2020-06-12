from flask import Flask, jsonify, render_template, request, redirect, session, Markup
from flask_googlemaps import Map
from flask_googlemaps import icons
import audio
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
    elif session['type']=='a':
        return render_template("admin/home.html", name=session.get('username'))
    elif session['type']=='e':
        return render_template("engineer/home.html", name=session.get('username'))
    else:
        return render_template("manager/home.html", name=session.get('username'))
    
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
    elif session['type']=='a':
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
    elif session['type']=='e':
        mark=[]
        cars=mainEngine.listBrokenCars()
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
        return render_template("engineer/carlist.html",cars=cars, gmap=gmap)

@app.route('/carhistory', methods=["POST"])
def carhistory():
    carID =  request.form['id']
    bookings = mainEngine.listCarBookingHistory(carID)
    return render_template("admin/carhistory.html",bookings=bookings)

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

@app.route('/updatecarpage', methods = ['POST'])
def updatecarpage():
    carID = request.form['id']
    car = mainEngine.getCarDetails(carID)
    return render_template('admin/updatecar.html', car=car)

@app.route('/updatecar', methods = ['POST'])
def updatecar():
    carID = request.form['id']
    name = request.form['name']
    bodytype = request.form['bodytype']
    colour = request.form['colour']
    seats = request.form['seats']
    location = request.form['location']
    cost = request.form['cost']
    availibility = request.form['availability']
    mainEngine.updateCar(carID, name, bodytype, colour, seats, location, cost, availibility)
    return redirect('/carlist')

@app.route('/updateuserpage', methods = ['POST'])
def updateuserpage():
    userID = request.form['id']
    user = mainEngine.getUserDetails(userID)
    return render_template('admin/updateuser.html', user=user)

@app.route('/updateuser', methods = ['POST'])
def updateuser():
    usernameDuplicate=False
    usernameInvalid=False
    userID = request.form['id']
    username = request.form['username']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    acc_type = request.form['type']
    user = mainEngine.getUserDetails(userID)

    if mainEngine.update_check_duplicate_username(userID, username) is False and mainEngine.check_isalnum_username(username) is False:
        mainEngine.updateUser(userID, username, password, fname, lname, email, acc_type)
        return redirect('/userlist')
    if mainEngine.update_check_duplicate_username(userID, username) is True:
        usernameDuplicate=True
    if mainEngine.check_isalnum_username(username) is True:
        usernameInvalid=True
    return render_template('admin/updateuser.html', user=user, usernameDuplicate=usernameDuplicate, usernameInvalid=usernameInvalid)
    
@app.route('/deletecar', methods = ['POST'])
def deletecar():
    carID = request.form['delete']
    mainEngine.deleteCar(carID)
    return redirect('/carlist')

@app.route('/userlist', methods=["GET"])
def users():
    users=mainEngine.listUsers()
    return render_template("admin/userlist.html",users=users)

@app.route('/searchuser', methods = ('GET', 'POST'))
def searchuser():
    users={}
    search=""
    column=""
    if request.method == 'POST':
        column = request.form['column']
        search = request.form['search']        
        users=mainEngine.searchUsers(column, search)
    return render_template("admin/searchuser.html", search=search, column=column, users=users)

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
    if session['type']=='c':
        return render_template("customer/searchcar.html", search=search, column=column, cars=cars)
    elif session['type']=='a':    
        return render_template("admin/searchcar.html", search=search, column=column, cars=cars)
    
@app.route('/searchcarbyvoice')
def searchcarbyvoice():
    cars={}
    search=""
    column=""
    while column != "make" or column != "body type" or column != "colour" or column != "seats" or column != "location" or column != "cost":
        column = audio.speechRecognition()
        if column == "make" or column == "body type" or column == "colour" or column == "seats" or column == "location" or column == "cost":
            search = audio.speechRecognition()
            cars=mainEngine.searchCars(column, search)
    return render_template("admin/searchcar.html", search=search, column=column, cars=cars)    
    
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

#########################################
# Testing area for graphs visualisation #
#########################################
# labels = [
#     'JAN', 'FEB', 'MAR', 'APR',
#     'MAY', 'JUN', 'JUL', 'AUG',
#     'SEP', 'OCT', 'NOV', 'DEC'
# ]

# values = [
#     967.67, 1190.89, 1079.75, 1349.19,
#     2328.91, 2504.28, 2873.83, 4764.87,
#     4349.29, 6458.30, 9907, 16297
# ]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500"]

@app.route('/bar')
def bar():
    bar_labels= mainEngine.getTop10Price()
    bar_values= mainEngine.getTop10BookingCountForPrice()
    return render_template('bar_chart.html', title='Our Most popular prices', max=17000, labels=bar_labels, values=bar_values)

@app.route('/line')
def line():
    line_labels=mainEngine.getDuration()
    line_values=mainEngine.getDurationBookingCount()
    return render_template('line_chart.html', title='Duration of bookings made by users', max=17000, labels=line_labels, values=line_values)

@app.route('/pie')
def pie():
    pie_labels = mainEngine.getTop10Make()
    pie_values = mainEngine.getTop10BookingCountForMake
    return render_template('pie_chart.html', title='Bookings made for the top 10 car makes', max=17000, set=zip(pie_values, pie_labels, colors))

###############################################
# End of Testing area for graphs visualisation#
###############################################