#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from config.Config import DevConfig

from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

from endpoints.UserEndpoint import users
app.register_blueprint(users, url_prefix="/users")
