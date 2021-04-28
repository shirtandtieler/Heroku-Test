# This module provides a way to centralize all global configurations
# (rather than cluttering the entry file)
# It's suggested as part of Miguel Grinberg's Flask Mega-Tutorial
import os

basedir = os.path.abspath(os.path.dirname(__file__))


def build_db_url(user=None, pw=None, host=None, port=None, db=None):
    # prioritize passed vars, then environment vars, then assume not included
    user = user or os.environ.get('DATABASE_USERNAME') or ""
    pw = pw or os.environ.get('DATABASE_PASSWORD') or ""
    host = host or os.environ.get('DATABASE_HOST') or ""
    port = port or os.environ.get('DATABASE_PORT') or ""
    db = db or os.environ.get('DATABASE') or "mydb"

    # based on: https://stackoverflow.com/a/20722229
    url = "postgresql://"
    if user or pw:
        url += user
        if pw:
            url += f":{pw}@"
    url += host  # if not provided, will just add empty string
    if port:
        url += f":{port}"
    url += f"/{db}"
    print(url)
    return url


class Config:
    """ Contains configuration variables for quick loading in the main app file """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'team3-secret-key-no-one-will-ever-guess123'
    # When uploaded to heroku, DATABASE_URL will be set.
    # For local testing, the fallback will be used (if listed)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or build_db_url("user", "sudowoodo", "localhost", "5432", "website_project")
    # When track is false, do not signal the application every time a change is about to be made in the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
