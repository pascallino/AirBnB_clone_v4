#!/usr/bin/python3
""" New engine DBStorage
linked to the MySQL database """

import models
from os import getenv
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from models.base_model import BaseModel, Base
from models import *
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
import MySQLdb


class DBStorage:
    """ class to manage all db connections and database
    intweractivity"""
    __engine = None
    __session = None

    def __init__(self):
        """initialization of variables, connections to database"""
        __user = getenv("HBNB_MYSQL_USER")
        __pwd = getenv("HBNB_MYSQL_PWD")
        __host = getenv("HBNB_MYSQL_HOST")
        __db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session
        (self.__session) all objects depending of
        the class name (argument cls)"""
        alldict = {}
        if not cls:
            classes = [User, State, City, Amenity, Place, Review]
            for item in classes:
                query = self.__session.query(item)
                for row in query:
                    clName = row.__class__.__name__
                    # key = f"{clName}.{row.id}"
                    key = "{}.{}".format(clName, row.id)
                    alldict[key] = row
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for row in query:
                clName = row.__class__.__name__
                # key = f"{clName}.{row.id}"
                key = "{}.{}".format(clName, row.id)
                alldict[key] = row
        return alldict

    def new(self, obj):
        """add a new row in the table
        """
        self.__session.add(obj)

    def save(self):
        """save and flush changes to the db
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete an row in the table
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload the database config
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """ cals remove method"""
        self.__session.close()

    def get(self, cls, id):
        """ retrieve all objects based on classes and ids"""
        classes = [User, State, City, Amenity, Place, Review]
        if cls not in classes:
            return None
        allobjects = models.storage.all(cls)
        for obj in allobjects.values():
            if (obj.id == id):
                return obj
        return None

    def count(self, cls=None):
        """
        counts the number of objects in storage
        """
        classes = [User, State, City, Amenity, Place, Review]
        if cls is None:
            count = 0
            for c in classes:
                count = count + len(models.storage.all(c).values())
        else:
            count = len(models.storage.all(cls).values())
        return count
