from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
import ulid

db = SQLAlchemy()

class Todo(db.Model):
    id = db.Column(db.String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_Completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }

