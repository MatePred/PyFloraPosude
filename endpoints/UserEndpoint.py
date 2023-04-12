from UserManagementApp import db, app
from flask import Blueprint, request, jsonify, Response
from flask import Flask, render_template, url_for, redirect
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from service.UserService import UserService
from flask_bcrypt import Bcrypt
import json
from datasource.entity.User import User


users = Blueprint('users', __name__)

bcrypt = Bcrypt(app)

userService = UserService()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        #existing_user_username = userService.getUserByName(username.data)
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class UserEndpoint:

    #@login_manager.user_loader
    #def load_user(user_id):
    #   return User.query.get(int(user_id))
        #return userService.getUserById(user_id)

    @staticmethod
    @users.route('/')
    def home():
        return render_template('home.html')

    @staticmethod
    @users.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        log = ""
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            #userDto = userService.getUserByName(form.username.data)
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('dashboard'))
                    log = ""
                else:
                    print("Incorrect password!")
                    log = "Incorrect password!"
            else:
                print("User does not exist!")
                log = "User does not exist!"
        return render_template('login.html', form=form, variable=log)

    @staticmethod
    @users.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

        return render_template('register.html', form=form)

    @staticmethod
    @users.route('/dashboard', methods=['GET', 'POST'])
    #@login_required
    def dashboard():
        return render_template('dashboard.html')

    @staticmethod
    @users.route('/home2', methods=['GET', 'POST'])
    def home2():
        return render_template('home2.html')

    @staticmethod
    @users.route("/", methods=['GET'])
    def getAllUsers():
        return json.dumps(userService.getAllUsers())









