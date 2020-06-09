import subprocess
import os

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