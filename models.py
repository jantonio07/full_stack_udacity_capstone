import os
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    return db


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


def create_all():
    db.create_all()


class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def getData(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f'<Venue name={self.name}>'


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String, nullable = False)
    # description = db.Column(db.String, nullable = False)
    w = db.Column(db.Integer, nullable=False)
    h = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String, nullable=False)
    imageKitId = db.Column(db.String, nullable=False)
    albumId = db.Column(db.Integer, db.ForeignKey('albums.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def getData(self):
        return {
            "id": self.id,
            "w": self.w,
            "h": self.h,
            "url": self.url,
            "albumId": self.albumId,
        }

    def __repr__(self):
        return f'<Artist url={self.url}>'
