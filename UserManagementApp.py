from config.Config import DevConfig
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

from endpoints.UserEndpoint import users
from endpoints.PlantEndpoint import plants
from endpoints.PyPosudeEndpoint import pyPosude
app.register_blueprint(users, url_prefix="/")
app.register_blueprint(plants, url_prefix="/plants")
app.register_blueprint(pyPosude, url_prefix="/pyPosude")
