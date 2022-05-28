from os import getenv, path, urandom
from dotenv import load_dotenv


class Settings:
    BASEDIR = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(BASEDIR, ".env"))

    # Flask Settings
    SECRET_KEY = getenv("SECRET_KEY", urandom(24))
    PORT = getenv("PORT", 80)
    DEBUG = getenv("DEBUG", False)
    TESTING = getenv("TESTING", False)
    ENV = getenv("ENV", "production")

    # APP Settings
    TITLE = getenv("TITLE", "Dolphin")
    BRIEF = getenv("BRIEF", "Snippet Organizer For Developers")
    AUTHOR = getenv("AUTHOR", "Big Cats Team")
    AUTHOR_URL = getenv("AUTHOR_URL", "https://bigcats.ml")
    SITE_URL = getenv("SITE_URL", "http://127.0.0.1:5000")

    # Database Settings
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///" + path.join(BASEDIR, "dolphin.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
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