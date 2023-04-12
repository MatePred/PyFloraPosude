from UserManagementApp import db
from enum import Enum


class UserTypeEnum(Enum):
    #OBSERVER = 1
    USER = 2
    ADMIN = 3



class UserType(db.Model):

    __tablename__ = 'user_type'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return str(self.__dict__)