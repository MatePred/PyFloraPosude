from UserManagementApp import db, app
from datasource.changelog.Changelog import ChangeLog as cl
from datasource.entity.UserType import UserType, UserTypeEnum
from datasource.entity.User import User
from datasource.dto.UserDto import UserDto
from flask_bcrypt import Bcrypt
from datasource.entity.Plant import Plant
from datasource.dto.PlantDto import PlantDto
from datasource.entity.PyFloraPosuda import PyFloraPosuda

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

            posuda = PyFloraPosuda()
            posuda.name = "test"


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

            plant2_DTO : PlantDto = PlantDto()
            plant2_DTO.name = "kaktus2"
            plant2_DTO.photoURL = "imgs/kaktus/kaktus.jfif"
            plant2: Plant = Plant.createPlantFromDto(plant2_DTO)

            plant3_DTO : PlantDto = PlantDto()
            plant3_DTO.name = "suncokret1"
            plant3_DTO.photoURL = "imgs/suncokret/suncokret.jog"
            plant3: Plant = Plant.createPlantFromDto(plant3_DTO)

            plant4_DTO : PlantDto = PlantDto()
            plant4_DTO.name = "suncokret2"
            plant4_DTO.photoURL = "imgs/suncokret/suncokret.jog"
            plant4: Plant = Plant.createPlantFromDto(plant4_DTO)


            #print(administrator)
            cl.add_params("insert-user-types", admin, user)
            cl.add_params("insert-admin", administrator)
            cl.add_params("insert-plant", plant1,plant2,plant3,plant4)
            cl.add_params("insert-posuda", posuda)

            # allTypes = UserType.query.all()
            # for type in allTypes:
            #     print(type)

            # observer = UserType.query.filter_by(type=1).one_or_none()
            # print(observer)
            # observer.name = "observer"
            # db.session.commit()

