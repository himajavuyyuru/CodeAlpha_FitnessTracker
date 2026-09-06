from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    assessments = db.relationship(
        "FitnessAssessment",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    activities = db.relationship(
        "FitnessActivity",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class FitnessAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    age = db.Column(db.Integer, nullable=False)

    height = db.Column(db.Float, nullable=False)

    weight = db.Column(db.Float, nullable=False)

    activity = db.Column(db.String(20), nullable=False)

    bmi = db.Column(db.Float, nullable=False)

    calories = db.Column(db.Integer, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )


class FitnessActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    date = db.Column(
        db.Date,
        default=datetime.utcnow().date,
        nullable=False
    )

    steps = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    workout_type = db.Column(
        db.String(100),
        nullable=False
    )

    duration = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    calories_burned = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )