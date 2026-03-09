import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Config:

    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    SECURITY_PASSWORD_SALT = 'your_password_salt_here'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "resumes")
    MAX_CONTENT_LENGTH = 500 * 1024 

