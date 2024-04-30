from os import getenv, path, urandom
from dotenv import load_dotenv


class Settings:
    BASEDIR = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(BASEDIR, ".env"))

    # Flask Settings
    SECRET_KEY = getenv("SECRET_KEY", "YmVuIGhhbGEgZG9sYXNpeW9ydW0gYXZhcmUuLi4=")
    PORT = getenv("PORT", 80)
    DEBUG = getenv("DEBUG", False)
    TESTING = getenv("TESTING", False)
    ENV = getenv("ENV", "production")

    # APP Settings
    TITLE = getenv("TITLE", "Dolphin")
    BRIEF = getenv("BRIEF", "Snippet Organizer For Developers")
    AUTHOR = getenv("AUTHOR", "Yunus Emre Geldegül")
    AUTHOR_URL = getenv("AUTHOR_URL", "https://emregeldegul.com.tr")
    SITE_URL = getenv("SITE_URL", "http://127.0.0.1:5000")

    # MySQL Settings
    MYSQL_SERVER_NAME: str = getenv("MYSQL_SERVER_NAME", "localhost")
    MYSQL_SERVER_PORT: int = getenv("MYSQL_SERVER_PORT", 3306)
    MYSQL_USER_NAME: str = getenv("MYSQL_USER_NAME", "root")
    MYSQL_USER_PASSWORD = getenv("MYSQL_USER_PASSWORD", "")
    MYSQL_DATABASE_NAME: str = getenv("MYSQL_DATABASE_NAME", "dolphin")

    # SQLAlchemy Database Settings
    SQLALCHEMY_DATABASE_URI = getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+pymysql://{user_name}:{user_password}@{server_name}:{server_port}/{database_name}".format(
            user_name=MYSQL_USER_NAME,
            user_password=MYSQL_USER_PASSWORD,
            server_name=MYSQL_SERVER_NAME,
            server_port=MYSQL_SERVER_PORT,
            database_name=MYSQL_DATABASE_NAME,
        ),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 20,
        "pool_recycle": 60,
        "pool_pre_ping": True
    }

    # Mail Settings
    MAIL_SERVER = getenv("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_PORT = getenv("MAIL_SERVER", 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD", "")


settings = Settings()
