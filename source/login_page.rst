.. _login_page:

Login Page
===========
*Directory: app/templates/login.html*

The login page is a html page that contains a form that takes in your username 
and password

How it works
-------------
loginPage() in :ref:`views` would receive the submitted information from the user 
and call login(username, password) in :ref:`main_engine`. If the login() function authenticates, 
the user credentials will be saved to the current session.

