from UserManagementApp import db, app
from datasource.changelog.Changelog import ChangeLog as cl
from datasource.entity.UserType import UserType, UserTypeEnum
from datasource.entity.User import User
from datasource.dto.UserDto import UserDto
from flask_bcrypt import Bcrypt
from datasource.entity.Plant import Plant
from datasource.dto.PlantDto import PlantDto

class InitializeService:

    def __init__(self):
        with app.app_context():
            db.create_all()

            bcrypt = Bcrypt(app)
            """
            observer = UserType()
            observer.type = UserTypeEnum.OBSERVER.value # 1
            observer.name = UserTypeEnum.OBSERVER.name.lower() # observer

            db.session.add(observer)
            db.session.commit()
            """
            # hint
            """
            observer: UserType = UserType.query.filter_by(id=2).one_or_none()
            if observer is not None:
                print(f"{observer.id}, {observer.name}, {observer.type}")
            else:
                print("None")
            """
            #observer = UserType()
            #observer.type = UserTypeEnum.OBSERVER.value
            #observer.name = UserTypeEnum.OBSERVER.name.lower()

            user = UserType()
            user.type = UserTypeEnum.USER.value
            user.name = UserTypeEnum.USER.name.lower()

            admin = UserType()
            admin.type = UserTypeEnum.ADMIN.value
            admin.name = UserTypeEnum.ADMIN.name.lower()

            #add administrator account to the table,
            #cannot be deleted
            administratorDTO = UserDto()
            administratorDTO.user_type = UserTypeEnum.ADMIN.value
            administratorDTO.username = "administrator"
            administratorDTO.pwd = bcrypt.generate_password_hash("12345678").decode("utf-8")
            administrator = User.createAdminUserFromDto(administratorDTO)

            #dodaj biljku
            plant1_DTO : PlantDto = PlantDto()
            plant1_DTO.name = "kaktus"
            plant1_DTO.photoURL = "imgs/kaktus/kaktus.jfif"
            plant1: Plant = Plant.createPlantFromDto(plant1_DTO)


            #print(administrator)
            cl.add_params("insert-user-types", admin, user)
            cl.add_params("insert-admin", administrator)
            cl.add_params("insert-plant", plant1)

            # allTypes = UserType.query.all()
            # for type in allTypes:
            #     print(type)

            # observer = UserType.query.filter_by(type=1).one_or_none()
            # print(observer)
            # observer.name = "observer"
            # db.session.commit()

