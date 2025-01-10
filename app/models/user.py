from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import db
import uuid

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), unique=True, nullable=False)
    lastName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)

    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    
    def __init__(self, firstName, lastName, email, password, role_id):
        self.public_id = str(uuid.uuid4())
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.set_password(password)
        self.role_id = role_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.firstName}>"
    
    def to_json_user(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
        }
    