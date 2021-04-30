# This module provides a way to centralize all global configurations
# (rather than cluttering the entry file)
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


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
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'team3-super-secret-key-omg'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              build_db_url(user="user", pw="password",
                                           host="localhost", port="5432",
                                           db="jobsite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')