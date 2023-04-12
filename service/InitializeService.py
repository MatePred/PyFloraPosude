from UserManagementApp import db, app
from datasource.changelog.Changelog import ChangeLog as cl
from datasource.entity.UserType import UserType, UserTypeEnum

class InitializeService:

    def __init__(self):
        with app.app_context():
            db.create_all()
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

            cl.add_params("insert-user-types", admin, user)

            # allTypes = UserType.query.all()
            # for type in allTypes:
            #     print(type)

            # observer = UserType.query.filter_by(type=1).one_or_none()
            # print(observer)
            # observer.name = "observer"
            # db.session.commit()

