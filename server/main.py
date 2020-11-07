from osmand import *
from flask import Flask, send_file
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/osmand/<int:zoom>/<int:x>/<int:y>.png')
def osmand(zoom, x, y):
    # return 'testing!'

    return send_file('fish.png', attachment_filename='python.jpg')
