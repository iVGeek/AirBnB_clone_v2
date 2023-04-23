class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        # Create a new session and initialize the attributes
        self.__session = scoped_session(sessionmaker(bind=self.__engine))()

    def all(self, cls=None):
        # Returns a dictionary of all objects
        objects_dict = {}
        if cls:
            for obj in self.__session.query(classes[cls]).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects_dict[key] = obj
        else:
            for cls in classes.values():
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects_dict[key] = obj
        return objects_dict

    def new(self, obj):
        # Add obj to the current session
        self.__session.add(obj)

    def save(self):
        # Commit all changes to the database
        self.__session.commit()

    def reload(self):
        # Create all tables in the database and create a new session
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
#!/usr/bin/python3
"""DB storage
"""
import models
from models.base_model import BaseModel, Base
from models import city, state
from os import environ, getenv
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')



