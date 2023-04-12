from UserManagementApp import db
from datetime import datetime as dt
from datasource.entity.UserType import UserTypeEnum
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


#class User(db.Model, UserMixin):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(20), nullable=False, unique=True)
#    password = db.Column(db.String(80), nullable=False)

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(30), nullable=False)
    #surname = db.Column(db.String(50), nullable=False)
    #email = db.Column(db.String(70), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    pwd = db.Column(db.String(80), nullable=False)
    user_type = db.Column(db.Integer, db.ForeignKey('user_type.type'), nullable=False)
    created = db.Column(db.String(20), nullable=False)

    @staticmethod
    def createUserFromDto(dto):
        user = User()
        #user.name = dto.name
        #user.surname = dto.surname
        #user.email = dto.email
        user.username = dto.username
        user.pwd = dto.pwd
        user.created = str(int(dt.now().timestamp()))
        user.user_type = UserTypeEnum.USER.value
        return user


