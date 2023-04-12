from UserManagementApp import db
from datetime import datetime as dt


class ChangeLog(db.Model):
    __tablename__ = 'changelog'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    created = db.Column(db.String(20), nullable=False)

    @staticmethod
    def add_params(name: str, *obj: object):
        log = ChangeLog.query.filter_by(name=name).all()
        successful = False
        if log is not None and len(log) > 0:
            print(len(log))
            print(log)
            return
        else:
            try:
                changelog = ChangeLog()
                for o in obj:
                    try:
                        db.session.add(o)
                        successful = True
                    except Exception as e:
                        print(e)
                        db.session.rollback()
                        successful = False

                    if successful:
                        changelog.name = name
                        changelog.created = str(int(dt.now().timestamp()))
                        db.session.add(changelog)

                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                raise