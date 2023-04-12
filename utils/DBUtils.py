from UserManagementApp import db

class DBUtils:

    @staticmethod
    def commit():
        db.session.commit()


    @staticmethod
    def insert(model):
        try:
            db.session.add(model)
            DBUtils.commit()
            return model
        except Exception as e:
            print(e)
            db.session.rollback()
            return None


    @staticmethod
    def findAll(clazz):
        return clazz.query.all()


    @staticmethod
    def findById(clazz, id):
        return clazz.query.filter_by(id=id).one_or_none()


    @staticmethod
    def deleteById(clazz, id):
        model = DBUtils.findById(clazz, id)
        if model is not None:
            return DBUtils.delete(model)
        else:
            return False


    @staticmethod
    def delete(model):
        try:
            db.session.delete(model)
            DBUtils.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False










