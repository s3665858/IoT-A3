.. _register_page:

Register Page
================
*Directory: app/templates/register.html*

The register page is a html page that contains a form that takes in your 
username, password, firstname, lastname and email

How it works
-------------
registerPage() in :ref:`views` would receive the submitted information from the user 
and call check_duplicate_username(username) and check_isalnum_username(username) in :ref:`main_engine`. 
If both functions is verified, then only register(username, password, fname, lname, email) 
in :ref:`main_engine` is called. If the verifications are not approved, an error message will 
be displayed accordingly and prompts the user to retry their registration.

