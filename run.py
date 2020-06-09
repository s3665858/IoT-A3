from app import app
import threading
import time
from server import SocketServer

def activate_job():
    def run_job():
        socket = SocketServer()
        socket.startListening()

    thread = threading.Thread(target=run_job)
    thread.start()
if __name__ == '__main__':
    activate_job()
    app.run(use_reloader=False)
    