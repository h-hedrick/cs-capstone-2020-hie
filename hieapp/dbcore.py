from hieapp import app 
from flask_sqlalchemy import SQLAlchemy

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/Users/Matt/Documents/GitHub/cs-capstone-2020-hie/hieapp/testdb.db"
db = SQLAlchemy(app)