from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)
    planet_favorites = relationship('FavoritePlanet', backref='User', lazy=True)
    character_favorites = relationship('FavoriteCharacter', backref='User', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'
    # Here we define columns for the table character.
    # Notice that each column is also a normal Python instance attribute.
    character_id = Column(Integer, unique=True,primary_key=True)
    character_homeworld = Column(String(250), nullable=False)
    character_name = Column(String(250)) 
    character_skill = Column(String(250), nullable=False)
    character_favorites = relationship('FavoriteCharacter', backref='Character', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.character_id

    def serialize(self):
        return {
            "character_id": self.character_id,
            "character_name": self.character_name,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    # Here we define columns for the table planet.
    # Notice that each column is also a normal Python instance attribute.
    planet_id = Column(Integer, unique=True,primary_key=True)
    planet_population = Column(Integer, nullable=False)
    planet_diameter = Column(Integer, nullable=False)
    planet_climate = Column(String(250), nullable=False)
    planet_name = Column(String(250))
    planet_favorites = relationship('FavoritePlanet', backref='Planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.planet_id

    def serialize(self):
        return {
            "planet_id": self.planet_id,
            "planet_name": self.planet_name,
            # do not serialize the password, its a security breach
        }
    
class FavoriteCharacter(db.Model):
    __tablename__ = 'favoritecharacter'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    character_id = Column(Integer, ForeignKey('character.character_id'))

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.user_id

    def serialize(self):
        user = User.query.get(self.user_id)
        return {
            "user": user.username,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favoriteplanet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    planet_id = Column(Integer, ForeignKey('planet.planet_id'))

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "id": self.id
            # do not serialize the password, its a security breach
        }
