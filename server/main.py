from flask import Flask, send_file
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/osmand/<int:x>/<int:y>/<int:file>.png')
def osmand(x, y, file):
    # return 'testing!'
    return send_file('fish.png', attachment_filename='python.jpg')
