from app.models.base_model import BaseModel
from app import db, bcrypt
from sqlalchemy.orm import validates
import uuid

import re


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships 
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy=True, cascade='all, delete-orphan')

    @validates("first_name")
    def validate_first_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("First name is required and must be under 50 characters")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Last name is required and must be under 50 characters")
        return value

    @validates("email")
    def validate_email(self, key, value):
        email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format")
        return value.lower()

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Password is required")
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)
