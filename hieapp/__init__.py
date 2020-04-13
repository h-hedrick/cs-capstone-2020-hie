from flask import Flask
from flask_cors import CORS

#set up flask application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
CORS(app)