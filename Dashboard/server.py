# Flask sever that listens to POSTs and emits to index page
# To serve [DEBUG]: FLASK_ENV=development FLASK_APP=server.py DEBUG=True flask run --host=0.0.0.0
from flask_socketio import SocketIO
from flask import Flask, request, render_template

app = Flask(__name__)
socketio = SocketIO(app)

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
	socketio.emit('data_stream',  {'gps_ts': gps_timestamp, 'res': res_id, 'lat': float(lat), 'lon': float(lon)})
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