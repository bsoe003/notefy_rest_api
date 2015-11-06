from flask import *
from api import app, models

@app.route('/')
def root():
    return jsonify({})