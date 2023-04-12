

class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///pyFloraPosude.sqlite3"
    DEBUG = True
    SECRET_KEY = "s9d8f7g0a987sdf0a98sd6f7654sad"
