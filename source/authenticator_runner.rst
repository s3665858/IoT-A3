.. _google_authenticator_runner:

Google Authenticator Runner
=============================
This authenticator runner is used to create a subprocess which would run the :ref:`api_authenticator`
and passes in the user's ID and authentication key to create a token file for the user.

run_authenticator(userID, key)
-----------------------------------
parameters: *userID*, *key*

function: runs the subprocess :ref:`api_authenticator` and then passing in the *userID* and *key* as an 
input for the running subprocess
::

    def run_authenticator(userID, key):
        input = str(userID) + '\n' + str(key) + '\n'
        input_as_bytes = bytes(input,'utf-8')
        read, write = os.pipe()
        os.write(write, input_as_bytes)
        os.close(write)
        try:
            subprocess.check_call(['python3','google_calendar/api_authenticator.py','--noauth_local_webserver'], stdin=read)
        except Exception:
            pass


