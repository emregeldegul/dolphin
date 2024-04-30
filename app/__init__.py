"""
Yunus Emre Geldegül, 22 Mart 2022 20:30
yunusemregeldegul@gmail.com

Ey yolcu dostum, ayakların rehberindir
Senin dostun soğuk esen yellerdir
Tüm insanlık senin gözünde eldir
İçecek suyun gözlerinden taşan seldir
Bu ödenecek bedeldir
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail

from settings import settings
from app.models.enums import Status

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def unauthorized(e):
    render_template("assets/errors/403.html"), 403


def page_not_found(e):
    return render_template("assets/errors/404.html"), 404


def international_server_error(e):
    db.session.rollback()
    return render_template("assets/errors/500.html"), 500


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please Login To Access This Page"
    login_manager.login_message_category = "info"

    app.register_error_handler(403, unauthorized)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, international_server_error)

    @app.context_processor
    def context_processor():
        from app.models.collection import Tag
        menu_tag_navigation = []

        if current_user.is_authenticated:
            menu_tag_navigation = Tag.query.filter_by(user=current_user).all()

        return dict(
            menu_tag_navigation=menu_tag_navigation,
        )

    from app.routes.main import main
    app.register_blueprint(main)

    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.profile import profile
    app.register_blueprint(profile)

    from app.routes.collection import collection
    app.register_blueprint(collection)

    return app
