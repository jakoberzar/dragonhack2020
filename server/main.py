from osmand import *
from sentinel import get_and_save_false_color_map
from flask import Flask, send_file
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/fireMap/fireMap.obf.zip')
def fireMap():
    return send_file('fireMap.obf.zip', attachment_filename='file.zip')


@app.route('/osmand/<int:zoom>/<int:x>/<int:y>.png')
def osmand(zoom, x, y):
    # return 'testing!'

    coords = getTileCoordinates(x, y, zoom)

    # for testing;
    # lat = 34.588986697590315
    # lon = -119.82341766357422
    # margin = 0.2
    # coords = [lon - margin, lat - margin, lon + margin, lat + margin]

    get_and_save_false_color_map(coords)
    return send_file('file.png', attachment_filename='file.jpg')
