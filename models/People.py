from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.dialects.mysql import BINARY

db = SQLAlchemy()


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    birthdate = db.Column(db.String(10), nullable=False)
    uuid = db.Column(BINARY(16), unique=True, default=uuid.uuid4().bytes, nullable=False)

    def __init__(self, firstname, lastname, birthdate):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate

    def current_jobs(self):
        return [job for job in self.jobs if job.end_date is None]

    def serialize(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birthdate': self.birthdate,
            'uuid': uuid.UUID(bytes=self.uuid)
        }
