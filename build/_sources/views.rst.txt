.. _views:

Views class
===============
*Directory: /app/views.py*

This class contains and manages all code from our controller :ref:`main_engine` to the html pages which are 
viewed by the user

Functions contained in this class:

registerPage()
---------------
function: receives all user information from the request form submitted by the user and calls checks input 
using check_duplicate_username() and check_isalnum_username() function from :ref:`main_engine`. 
If the functions returns false, calls register() function from :ref:`main_engine`.
::

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


loginPage()
---------------
function: receives username and password from the request form submitted by the user and calls the 
login() function from :ref:`main_engine`. If login succeeds, redirects user to the home page, else 
returns an error.
::

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


home()
---------
function: render the username of the session into the home.html template of either customer or admin, engineer 
depending on their session type being either  session['type']=='c', 'a', or 'e'. This will redirect the user to
their respective home.html page.
::

    @app.route('/home')
    def home():
        if session['type']=='c':
            return render_template("customer/home.html", name=session.get('username'))
        else:
            return render_template("admin/home.html", name=session.get('username'))

cars()
---------------
function: render all car information including its Google Map API location into the carlist.html template 
of either customer or admin
::

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


addcar()
---------------
function: adds all car information from the request form in addcar.html and adds them into the database 
using insertCar() from :ref:`main_engine`.
::

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


set_car_availability_to_unavailable()
---------------------------------------
function: sets car availability to unavailable by modifying information in the database 
using setCarAvailability() from :ref:`main_engine`.
::

    @app.route('/set_car_availability_to_unavailable', methods = ['POST'])
    def set_car_availability_to_unavailable():
        carID = request.form['switch_to_unavailable']
        mainEngine.setCarAvailability(carID, 0)
        return redirect('/carlist')

set_car_availability_to_available()
---------------------------------------
function: sets car availability to available by modifying information in the database 
using setCarAvailability() from :ref:`main_engine`.
::

    @app.route('/set_car_availability_to_available', methods = ['POST'])
    def set_car_availability_to_available():
        carID = request.form['switch_to_available']
        mainEngine.setCarAvailability(carID, 1)
        return redirect('/carlist')


deletecar()
---------------
function: deletes a car from the car table in the database using deleteCar() from :ref:`main_engine`.
::

    @app.route('/deletecar', methods = ['POST'])
    def deletecar():
        carID = request.form['delete']
        mainEngine.deleteCar(carID)
        return redirect('/carlist')

updatecarpage()
---------------
Updates the car page by calling getCarDetails() from :ref:`main_engine`.

updatecar()
---------------
Allows an admin to update a car's specifications by calling updateCar() from :ref:`main_engine`.


users()
---------------
function: lists all users in the user table in the database using listUsers() from :ref:`main_engine`.
::

    @app.route('/userlist', methods=["GET"])
    def users():
        users=mainEngine.listUsers()
        return render_template("admin/userlist.html",users=users)

updateuser()
---------------
Allows an admin to update user details by calling updateCar() from :ref:`main_engine`.


deleteuser()
---------------
function: deletes a user from the user table in the database using deleteUser() from :ref:`main_engine`.
::

    @app.route('/deleteuser', methods = ['POST'])
    def deleteuser():
        userID = request.form['delete']
        mainEngine.deleteUser(userID)
        return redirect('/userlist')

searchcar()
---------------
function: search for a car in the car table in the database using searchCars() from :ref:`main_engine`.
::

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


history()
---------------
function: lists the booking history of the user in the current session from the database using 
listPersonalBookingHistory() and listCars() from :ref:`main_engine`.
::

    @app.route('/bookhistory')
    def history():
        bookings = mainEngine.listPersonalBookingHistory(session['userID'])
        cars=mainEngine.listCars()
        return render_template("customer/bookhistory.html", cars=cars, bookings=bookings)


makebooking()
---------------
function: receives the car information from the booking page and validate the booking first with 
insert_booking() from :ref:`google_calendar`, if validation succeeds, calls insertBooking() and setCarAvailability()
from :ref:`main_engine`.
::

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


upload_file()
---------------
function:  from :ref:`main_engine`.
::

    @app.route('/uploader',  methods = ['POST'])
    def upload_file():
        userID = session['userID']
        print(session['userID'])
        f = request.files['file']
        s = SocketServer()
        s.createEncoding(f,userID)
        return redirect('/home')


booking()
---------------
function: lists all the booking of the user of the current session using listPersonalOngoingBooking() 
and listCars() from :ref:`main_engine`.
::

    @app.route('/booking')
    def booking():
        bookings = mainEngine.listPersonalOngoingBooking(session['userID'])
        cars=mainEngine.listCars()
        return render_template("customer/booking.html", cars=cars, bookings=bookings)


deletebooking()
-----------------
function: cancels a booking speficied and owned by the user from the booking table by calling 
setCarAvailability() and setBookingOngoing() from :ref:`main_engine`. It also calls delete_booking() 
from :ref:`google_calendar`.
::

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


googleAuthenticate()
---------------------
function: receives userID and the google authentication key from the user and calls run_authenticator() function 
from :ref:`google_authenticator_runner`, if authentication succeeds, displays a success message from 
googleAuthenticationComplete() function. Else, prompts the user to try again.
::

    @app.route('/googleAuthenticate', methods = ('GET', ('POST')))
    def googleAuthenticate():
        if request.method == 'POST':
            code = request.form['code']
            userID = session['userID']
            run_authenticator(userID,code)
            return redirect("/googleAuthenticationComplete")
        else:
            return render_template("customer/googleAuthentication.html")


googleAuthenticationComplete()
----------------------------------
function: displays a success message when the user successfully authenticates their google account.
::

    @app.route('/googleAuthenticationComplete')
    def googleAuthenticationComplete():
        return render_template("customer/googleAuthenticationComplete.html")



repair()
----------------------------------
Returns a list of the Ongoing Repairs for the engineer with a list of cars using listCars() which redirects the engineer to repair.html
It Calls listCars() and listPersonalOngoingRepairs() from :ref:`main_engine`.

cancelrepair()
----------------------------------
The engineer has the option to cancel an ongoing repair where the repair status is changed to '2' meaning it is not undergoing repair by calling 
setCarAvailability() and setRepairStatus() from :ref:`main_engine`.
from :ref:`google_calendar`.


users()
----------------------------------
Returns a list users in the system for admins to monitor by calling 
listUsers() from :ref:`main_engine`. This is rendered by userlist.html.


searchuser()
----------------------------------
Creates the ability for admins to search for a user in the database based on username, first name, last name, email and user type.
This will create a list and display the results returned by calling 
searchUsers() from :ref:`main_engine`.

deleteUser()
----------------------------------
Allow an admin to delete a user from the system by calling 
deleteUser() from :ref:`main_engine`.


searchcar()
----------------------------------
Creates the ability for customers and admins to search for a car based on make, body_type, colour, seats, location and cost by calling 
searchCars() from :ref:`main_engine`.

The results are retuned as a form and are displayed as available, unavailable, or broken. It also denotes if the car is being rented.
This function is rendered by the searchcar.html page where they can report, update, or delete a car. This is rendered by searchcar.html.


searchcarbyvoice()
----------------------------------
Allows a user to search for a car using speech recognition. This function detects speech and recognises the make, body type, colour, cost or location etc.
Then it returns a list of the results by calling searchCars() from :ref:`main_engine`. This is rendered by searchcar.html.


history()
----------------------------------
Returns a list of the booking history of a customer by calling listCars() from :ref:`main_engine`. This is rendered by bookhistory.html.

repairhistory()
----------------------------------
Returns a list of the personal repairs history of an engineer by calling listCars() from :ref:`main_engine`. This is rendered by repairhistory.html.

addmacaddress()
----------------------------------
An engineer is able to assign a MAC address by calling getEngineerAddress() and insertEngineer() from :ref:`main_engine`. This is rendered by addmacaddress.html.


deleteMacAddress()
----------------------------------
An engineer can delete a MAC address assigned to an engineer by calling deleteAdress() from :ref:`main_engine`.


carHistory()
----------------------------------
Allows the admin to view a list of the car booking history by calling listCarBookingHistory() from :ref:`main_engine`.

