from flask_security import SQLAlchemyUserDatastore
from controllers.model import User,Role

from controllers.database import db

user_datastore=SQLAlchemyUserDatastore(db,User,Role)