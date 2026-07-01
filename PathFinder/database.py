from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#########################################################
# USER TABLE
#########################################################

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fullname = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    age = db.Column(
        db.Integer
    )

    country = db.Column(
        db.String(100)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

#########################################################
# QUIZ RESULTS
#########################################################

class QuizResult(db.Model):

    __tablename__ = "quiz_results"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    personality = db.Column(
        db.String(100)
    )

    interests = db.Column(
        db.Text
    )

    skills = db.Column(
        db.Text
    )

    values = db.Column(
        db.Text
    )

    compatibility = db.Column(
        db.Float
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

#########################################################
# SAVED CAREERS
#########################################################

class SavedCareer(db.Model):

    __tablename__ = "saved_careers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    career_name = db.Column(
        db.String(250)
    )

    compatibility = db.Column(
        db.Float
    )

    salary = db.Column(
        db.String(100)
    )

    university = db.Column(
        db.String(250)
    )

#########################################################
# CHAT HISTORY
#########################################################

class ChatMessage(db.Model):

    __tablename__ = "chat_messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    sender = db.Column(
        db.String(20)
    )

    message = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

#########################################################
# BADGES
#########################################################

class Badge(db.Model):

    __tablename__ = "badges"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    badge_name = db.Column(
        db.String(100)
    )

    earned_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

#########################################################
# UNIVERSITY LIKES
#########################################################

class FavoriteUniversity(db.Model):

    __tablename__ = "favorite_universities"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    university_name = db.Column(
        db.String(250)
    )

#########################################################
# ACHIEVEMENTS
#########################################################

class Achievement(db.Model):

    __tablename__ = "achievements"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    title = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

#########################################################
# CAREER REPORTS
#########################################################

class CareerReport(db.Model):

    __tablename__ = "career_reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    career = db.Column(
        db.String(250)
    )

    report = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

#########################################################
# USER SETTINGS
#########################################################

class UserSettings(db.Model):

    __tablename__ = "user_settings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    dark_mode = db.Column(
        db.Boolean,
        default=True
    )

    notifications = db.Column(
        db.Boolean,
        default=True
    )

    language = db.Column(
        db.String(50),
        default="English"
    )

#########################################################
# USER PROGRESS
#########################################################

class UserProgress(db.Model):

    __tablename__ = "user_progress"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    quizzes_completed = db.Column(
        db.Integer,
        default=0
    )

    careers_saved = db.Column(
        db.Integer,
        default=0
    )

    chatbot_questions = db.Column(
        db.Integer,
        default=0
    )

#########################################################
# DATABASE INITIALIZER
#########################################################

def initialize_database(app):

    db.init_app(app)

    with app.app_context():

        db.create_all()

        print("Database initialized successfully.")