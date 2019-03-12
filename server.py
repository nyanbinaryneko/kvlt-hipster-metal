import os
from flask import flask

app = Flask(__name__)
app.run(environ.get(host='0.0.0.0',port=environ.get('PORT')))
