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
from datasource.entity.UserType import UserTypeEnum


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

class ModifyUserForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Modify')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Username"})

    submit = SubmitField('Login')

class UserEndpoint:

    @staticmethod
    @users.route('/')
    def home():
        return render_template('index.html')

    @staticmethod
    @users.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        log = ""
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            #administrator   12345678

            if user:
                try:
                    if bcrypt.check_password_hash(user.pwd, form.password.data):
                        login_user(user)
                        if user.user_type == UserTypeEnum.ADMIN.value:
                            return redirect(url_for('users.adminPanel'))
                        else:
                            return redirect(url_for('users.dashboard'))
                        log = ""
                    else:
                        print("Incorrect password!")
                        log = "Incorrect password!"
                except:
                    print("An exception occurred")
                    log = "An exception occurred"

            else:
                print("User does not exist!")
                log = "User does not exist!"
        return render_template('login.html', form=form, variable=log)

    @staticmethod
    @users.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user_data = {
                'username': form.username.data,
                'pwd': hashed_password
            }
            new_user = userService.createUser(json.dumps(user_data))
            return redirect(url_for('users.login'))

        return render_template('register.html', form=form)

    @staticmethod
    @users.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():
        return render_template('listaPosuda.html')

    @staticmethod
    @users.route('/adminPanel', methods=['GET', 'POST'])
    @login_required
    def adminPanel():
        #ucitaj sve usere iz baze u listu i predaj ju templateu

        selected_option = None
        form = ModifyUserForm()

        #print(request.method)
        if request.method == 'POST':
            if 'option' in request.form:
                selected_option = request.form['option']

            if form.validate_on_submit() and selected_option is not None:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
                user_data = {
                    'username': form.username.data,
                    'pwd': hashed_password
                }
                # check if modified username allready is used in database
                # but not in a user you want to mofiy - in that way you are able
                #to modify password only
                usernames = userService.getAllUsersNames()
                usernames.remove(selected_option)

                if user_data['username'] not in usernames :
                    user_to_mod = userService.getUserByName(selected_option)
                    userService.updateUser(json.dumps(user_data),user_to_mod['id'])
                else:
                    print("Username allready exist.")

            if 'SbmBtn_DeleteUser' in request.form:
                if(selected_option):
                    if selected_option != "administrator":
                        userService.deleteUserByName(selected_option)
                    print(selected_option)

        options = userService.getAllUsersNames()
        options.remove("administrator")
        return render_template('adminPanel.html', options=options,selected_option=selected_option,form=form)

    @staticmethod
    @users.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('users.login'))

    @staticmethod
    @users.route("/", methods=['GET'])
    def getAllUsers():
        return json.dumps(userService.getAllUsers())









