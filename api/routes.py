#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import *
from api import app, models
from wrappers import Notefy
from datetime import datetime
import os

notefy = Notefy(dictionary='dictionary/cellFirst10Page.txt')
images = set()

@app.route('/')
def root():
    return jsonify({})

@app.route('/addImage', methods=["GET", "POST"])
def addImage():
    if request.method != "POST":
        body = json.dumps({"error": request.method+" method is not allowed."})
        return Response(body, status=405, mimetype='application/json')
    if "filename" not in request.args:
        body = json.dumps({"error": "Missing required argument"})
        return Response(body, status=422, mimetype='application/json')
    images.add(request.args["filename"]+"\n")
    f = open('images.txt', 'w')
    f.writelines(list(images))
    f.close()
    return Response(json.dumps({}), status=200, mimetype='application/json')

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
    if "error" in downloaded:
        notefy.clean()
        return Response(json.dumps(downloaded), status=409, mimetype='application/json')

    # Perform OCR through a9t9/Microsoft service
    try:
        content = notefy.sendToOCR()
        print "OCR Completed"
    except:
        notefy.clean()
        body = json.dumps({"error": "There seems to be an error while performing OCR"})
        return Response(body, status=409, mimetype='application/json')

    print "Auto-correcting string"
    # formatted = notefy.sf.formatting(content.encode('ascii', 'ignore'))
    # content = formatted["content"]
    content = notefy.sf.formatting(content.encode('ascii', 'ignore'))

    print "Looking through Wikipedia"
    # entries = set()
    splitted, entries, keyterms = content.split(), [], []
    for i in range(len(splitted)):
    # for term in formatted["keyterms"]:
        if not notefy.isKeyterm(splitted[i]):
            continue
        try:
            entry = notefy.engine.find(splitted[i].lower())
            if entry.__dict__ not in entries:
                entries.append(entry.__dict__)
            if entry.title.lower() != splitted[i].lower():
                continue
            # entries.add(notefy.engine.find(splitted[i]))
            if splitted[i].lower() not in keyterms:
                keyterms.append(splitted[i].lower())
            index = keyterms.index(splitted[i].lower())+1
            splitted[i] += " [%s]" % str(index)
        except:
            continue

    print "Foramtting output"
    # entries = list(entries)
    content = " ".join(splitted)
    # for i in range(len(entries)):
        # entries[i] = entries[i].__dict__
    content = notefy.sf.prettyPrint(content, entries, keyterms)

    # create sample output text (soon to be changed)
    if "course" in request.args:
        title = request.args["course"]+"_"+str(datetime.now())+".txt"
    else:
        title = "UNKNOWN_"+str(datetime.now())+".txt"

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
