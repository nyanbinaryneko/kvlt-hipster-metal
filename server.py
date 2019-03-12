import os
from flask import flask

app = Flask(__name__)
app.run(os.environ.get(host='0.0.0.0',port=os.environ.get('PORT')))
