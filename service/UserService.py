from datasource.dto.UserDto import UserDto
from datasource.entity.User import User
from UserManagementApp import db
from utils.DBUtils import DBUtils
import uuid


class UserService:

    def __init__(self):
        pass


    def createUser(self, userData):
        print(userData)
        userDto = UserDto().serialize(userData, ignoreProperties=False)
        print(userDto)
        user = User.createUserFromDto(userDto)
        user = DBUtils.insert(user)
        if user is not None:
            newUserDto = UserDto.createFromEntity(user)
            # userType = userTypeService.getUserTypeByType(1)
            # newUserDto.userType = userType.name
            return newUserDto.getJson()

        return None


    def getAllUsers(self):
        userDtoList = []
        users = DBUtils.findAll(User)
        for u in users:
            userDtoList.append(UserDto.createFromEntity(u).getJson())
        return userDtoList


    def getUserById(self, id):
        user = DBUtils.findById(User, id)
        if user is not None:
            return UserDto.createFromEntity(user).getJson()

        return None

    def getUserByName(self, name):
        user = User.query.filter_by(username=name).first()
        if user is not None:
            return UserDto.createFromEntity(user).getJson()

        return None

    def deleteUserById(self, id):
        return DBUtils.deleteById(User, id)


    def updateUser(self, userData, id, token):
        userDto: UserDto = UserDto().serialize(userData, ignoreProperties=False)
        user: User = DBUtils.findById(User, id)
        # dohvatite token po value-u
        # provjerite toke.user_id == id

        updated = False
        if user is not None:
            if userDto.name is not None and user.name != userDto.name:
                user.name = userDto.name
                updated = True

            if userDto.surname is not None and user.surname != userDto.surname:
                user.surname = userDto.surname
                updated = True

            if userDto.email is not None and user.email != userDto.email:
                user.email = userDto.email
                updated = True

            if userDto.username is not None and user.username != userDto.username:
                user.username = userDto.username
                updated = True

            if updated:
                DBUtils.commit()
                newUserDto = UserDto.createFromEntity(user)
                return updated, newUserDto.getJson()

            return updated, UserDto.createFromEntity(user).getJson()

        return False, None


