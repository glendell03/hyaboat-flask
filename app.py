# sudo chmod a+rw /dev/ttyACM0
from flask import Flask, Response
from flask_socketio import SocketIO
import json
from arduino.relay import Relay


app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return "hEllo"


@socketio.on("coords")
def getCoords(data):
    relay = Relay()
    loaded_data = json.loads(data)
    


if __name__ == "__main__":
    socketio.run(app)
