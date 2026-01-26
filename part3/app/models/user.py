from app.models.base_model import BaseModel
from app import db, bcrypt
from uuid

import re

class User(BaseModel):
        __tablename__ = 'users'
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        self.password = None
        if password is not None:
            self.hash_password(password)
            
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)


    # --- Getter & Setter for first_name ---

    @first_name.setter
    def first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("First name is required and must be under 50 characters")
        self._first_name = value

    # --- Getter & Setter for last_name ---
    @property
    def last_name(self):
        return self.last_name

    @last_name.setter
    def last_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Last name is required and must be under 50 characters")
        self._last_name = value

    # --- Getter & Setter for email ---
    @property
    def email(self):
        return self.email

    @email.setter
    def email(self, value):
        email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format")
        self._email = value

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Password is required")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)
