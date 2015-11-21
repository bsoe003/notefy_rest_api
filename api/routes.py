from flask import *
from api import app, models
from wrappers import Notefy, spelling
import time

notefy = Notefy()
notefy.speller = spelling.Speller('dictionary/cellFirst10Page.txt')

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
	if "filename" not in request.args:
		body = json.dumps({"error": "Missing required argument"})
		return Response(body, status=422, mimetype='application/json')

	# download image from Google Drive
	downloaded = notefy.download(request.args["filename"])
	# downloaded = notefy.download(request.args["fileID"]) # try using 0B0HnBs236F_YLVF1X0E0NVhHOG8
	if "error" in downloaded:
		notefy.clean()
		return Response(json.dumps(downloaded), status=409, mimetype='application/json')

	# Perform OCR through a9t9/Microsoft service
	try:
		content = notefy.sendToOCR()
	except:
		notefy.clean()
		body = json.dumps({"error": "There seems to be an error while performing OCR"})
	 	return Response(body, status=409, mimetype='application/json')

	content = content.split()
	entries = set()
	for i in range(len(content)):
		if not notefy.isKeyterm(content[i]):
			continue
		content[i] = notefy.speller.correct(content[i].strip())
		try:
			entries.add(str(notefy.engine.find(content[i])))
		except:
			continue
	content = ' '.join(content)
	content += "\n\n%s" % ("\n".join(list(entries)))

	# create sample output text (soon to be changed)
	title = "BILD1_"+str(int(time.time()))+".txt"

	# upload the text file to Google Drive
	uploaded = notefy.upload(title, content)
	if "error" in uploaded:
		notefy.clean()
		return Response(json.dumps(uploaded), status=409, mimetype='application/json')

	# finishing touches
	notefy.clean()
	body = json.dumps({
		"message": "Note has been created successfully and is now saved under Google Drive",
		"uploaded": "error" not in uploaded,
		"downloaded": "error" not in downloaded
	})
	return Response(body, status=200, mimetype='application/json')
