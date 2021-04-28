# This module provides a way to centralize all global configurations
# (rather than cluttering the entry file)
# It's suggested as part of Miguel Grinberg's Flask Mega-Tutorial
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'team3-secret-key-no-one-will-ever-guess123'
    # Used by SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # When track is false, do not signal the application every time a change is about to be made in the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
