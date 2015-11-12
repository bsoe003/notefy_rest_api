from flask import *
from api import app, models
from drive import Drive
import os

@app.route('/')
def root():
    return jsonify({})

@app.route("/alert", methods=["GET", "POST"])
def alert():
	if request.method != "POST":
		body = json.dumps({"error": request.method+" method is not allowed."})
		return Response(body, status=405, mimetype='application/json')
	if "token" not in request.args:
		body = json.dumps({"error": "Missing client token."})
		return Response(body, status=401, mimetype='application/json')
	if request.args["token"] != "Nadir001":
		body = json.dumps({"error": "Invalid token"})
		return Response(body, status=401, mimetype='application/json')
	if "fileID" not in request.args:
		body = json.dumps({"error": "Missing required argument"})
		return Response(body, status=422, mimetype='application/json')
	driver = Drive()
	fileID = request.args["fileID"] # try using 0B0HnBs236F_YLVF1X0E0NVhHOG8
	filename = "image_cache/"+fileID+".jpg"
	success = driver.download(fileID, open(filename, 'w'))
	if success:
		body = json.dumps({"message": "Download successful"})
		return Response(body, status=200, mimetype='application/json')
	else:
		os.remove(filename)
		body = json.dumps({"error": "There seems to be an error while downloading"})
		return Response(body, status=409, mimetype='application/json')
