# Flask sever to listen to POSTs
# To serve: FLASK_APP=server.py flask run --host=0.0.0.0
from flask import Flask
from flask import request
 
app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def rootPathHandler():
    print("Root path reached. Handler on /dev...")
    return "Root path reached. Handler on /dev..."
 
@app.route("/dev", methods = ['POST'])
def postJsonHandler():
    content = request.get_json()
    print("JSON content: {}".format(content))
    return "JSON data received"

if __name__ == '__main__':
	app.run(host='0.0.0.0')