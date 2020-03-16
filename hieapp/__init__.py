from flask import Flask
# from hieapp.dbcore import db

#set up flask application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

# from hieapp.dbcore import db