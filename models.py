from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(80), unique=True,
#                            nullable=False)
#     last_name = db.Column(db.String(80), unique=True,
#                           nullable=False)
#     email = db.Column(db.String(120), unique=True,
#                       nullable=False)
#     user_password = db.Column(db.String(120), unique=True,
#                               nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# def __repr__(self):
#     return f'User({self.first_name}, {self.last_name})'
#


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,
                         nullable=False)
    email = db.Column(db.String(120), unique=True,
                      nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'User({self.username}, {self.email})'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'User({self.first_name}, {self.last_name}) Review({self.title}, {self.content})'
        # return f'Review({self.title}, {self.content})'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'),
                          nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Comment({self.content})'
