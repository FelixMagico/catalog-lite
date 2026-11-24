from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager

ROLE_USER = "user"
ROLE_ADMIN = "admin"

PENDING = "pending"
APPROVED = "approved"
REJECTED = "rejected"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default=ROLE_USER)

    requests = db.relationship("InstallRequest", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False, default="")

    requests = db.relationship("InstallRequest", back_populates="application")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class InstallRequest(db.Model):
    __tablename__ = "install_requests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=False
    )
    status = db.Column(db.String(10), nullable=False, default=PENDING)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="requests")
    application = db.relationship("Application", back_populates="requests")


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
