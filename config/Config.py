

class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    # username = user2
    # password = 123pwd!
    # dbName = "mojabazaProdukcija"
    # mysql+pymysql://{username}:{password}@localhost:3306/{dbName}
    DEBUG = False


class DevConfig(Config):
    # pymysql - lib
    # username = user
    # password = pwd123
    # dbName = "mojabaza"
    # mysql+pymysql://{username}:{password}@localhost:3306/{dbName}
    SQLALCHEMY_DATABASE_URI = "sqlite:///user_management.sqlite3"
    DEBUG = True
    SECRET_KEY = "s9d8f7g0a987sdf0a98sd6f7654sad"
