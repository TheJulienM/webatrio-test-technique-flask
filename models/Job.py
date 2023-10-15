from flask_sqlalchemy import SQLAlchemy
from models.People import People, db


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(80), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    people = db.relationship('People', backref=db.backref('jobs', lazy=True))
