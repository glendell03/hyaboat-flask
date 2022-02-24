from flask import Flask, Response
from flask_socketio import SocketIO
import json


app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return "hEllo"


@socketio.on("coords")
def getCoords(data):
    loaded_data = json.loads(data)
    print(loaded_data)


if __name__ == "__main__":
    socketio.run(app)
