from flask import *
from api import app, models
from drive import Drive
import os
import requests
import time

@app.route('/')
def root():
    return jsonify({})

@app.route("/alert", methods=["GET", "POST"])
def alert():
	# sanity checks
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
	
	driver = Drive() # instantiate Google Drive instance

	# download image from Google Drive
	fileID = request.args["fileID"] # try using 0B0HnBs236F_YLVF1X0E0NVhHOG8
	imageFile = "image_cache/"+fileID+".jpg"
	downloaded = driver.download(fileID, open(imageFile, 'w'))
	if not downloaded:
		os.remove(imageFile)
		body = json.dumps({"error": "There seems to be an error while downloading"})
		return Response(body, status=409, mimetype='application/json')

	# Perform OCR through a9t9/Microsoft service
	ocrData = {"apikey": "helloworld", "language": "eng"}
	files = {"file": open(os.getcwd()+"/"+imageFile, 'rb')}
	try:
		ocrResponse = requests.post("https://ocr.a9t9.com/api/Parse/Image", data=ocrData, files=files)
		print "\nOCR Result:\n"+str(ocrResponse.json()["ParsedResults"][0]["ParsedText"])
		parsedText = ocrResponse.json()["ParsedResults"][0]["ParsedText"]
	except:
		body = json.dumps({"error": "There seems to be an error while performing OCR"})
		return Response(body, status=409, mimetype='application/json')

	# create sample output text (soon to be changed)
	title = str(int(time.time()))
	try:
		f = open("text_cache/"+title+".txt", 'w')
		f.write(parsedText)
		f.close()
	except:
		body = json.dumps({"error": "Unable to create notes"})
		return Response(body, status=409, mimetype='application/json')

	# upload the text file to Google Drive
	uploaded = driver.upload(title, "", "text/plain", "text_cache/"+title+".txt")
	if not uploaded:
		os.remove(imageFile)
		os.remove("text_cache/"+title+".txt")
		body = json.dumps({"error": "There seems to be an error while uploading"})
		return Response(body, status=409, mimetype='application/json')

	# finishing touches
	os.remove(imageFile)
	os.remove("text_cache/"+title+".txt")
	body = json.dumps({
		"message": "Note has been created successfully and is now saved under Google Drive",
		"uploaded": uploaded,
		"downloaded": downloaded
	})
	return Response(body, status=200, mimetype='application/json')
