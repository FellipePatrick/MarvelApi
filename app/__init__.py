from flask import Flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.debug = True


db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)



from app.controllers import default
from app.models import tables, forms

