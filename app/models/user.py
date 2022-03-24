from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.models.abstract import BaseModel
from app.models.enums import Status


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(status=Status.active).filter_by(id=id).first()


class User(BaseModel, UserMixin):
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    full_name = db.column_property(first_name + " " + last_name)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(70), nullable=False, unique=True)
    note = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.active)

    def __repr__(self):
        return "User({})".format(self.email)

    def generate_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
