from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):
        """Kept for compatibility; ORM handles timestamps via onupdate."""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update the attributes from dict and bump updated_at"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
