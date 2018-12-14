# Flask sever that listens to POSTs and emits to index page
# To serve [DEBUG]: FLASK_ENV=development FLASK_APP=server.py DEBUG=True flask run --host=0.0.0.0
from gmplot import gmplot
from flask_socketio import SocketIO
from flask import Flask, request, render_template

app = Flask(__name__)
socketio = SocketIO(app)

# Google Maps JavaScript API key
APIKEY = 'AIzaSyBKw8yu7hpiwYnN66qNcSqcnh8KvjH6Hw8'

# Place a marker on Google Maps and save page
def googleMapsRender(gps_ts, lat, lon, res_id, mcolor=None, mtext=None):
	gmap = gmplot.GoogleMapPlotter(float(lat), float(lon), 15, apikey=APIKEY)
	if res_id == '0':
		# Request for ration
		mcolor = 'yellow'
		mtext = "Trans. Time: {}\\nCoordinates: {}, {}\\nResource: Ration".format(gps_ts, lat, lon)
	elif res_id == '1':
		# Request for shelter
		mcolor = 'green'
		mtext = "Trans. Time: {}\\nCoordinates: {}, {}\\nResource: Shelter".format(gps_ts, lat, lon)
	elif res_id == '2':
		# Request for medical aid
		mcolor = 'red'
		mtext = "Trans. Time: {}\\nCoordinates: {}, {}\\nResource: Medical Aid".format(gps_ts, lat, lon)
	gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
	gmap.marker(float(lat), float(lon), color=mcolor, title=mtext)
	gmap.draw("static/map.html")

# Root handler renders index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Inlet handler handles POSTS and updates
# index page. Processing done on both sides 
# of the application (server and client).
@app.route('/inlet', methods=['POST'])
def inletHandler():
	content = request.data.decode('utf-8').split(',')
	device_id = content[0]
	gps_timestamp = content[1]
	lat = content[2]
	lon = content[3]
	res_id = content[4]
	socketio.emit('data_stream',  {'data': res_id})
	googleMapsRender(gps_timestamp, lat, lon, res_id)
	return "OK"

# Prevent cached responses
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')