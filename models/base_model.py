#!/usr/bin/python3
""" base model super class to be used
by allsub classes """

from uuid import uuid4
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
import models


if getenv('HBNB_TYPE_STORAGE') == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """ Basmodel for other classes save __str__ new
    All other classes will inherit from BaseModel to get common
    values (id, created_at, updated_at), where inheriting from
    ase will actually cause SQLAlchemy to attempt to map it to a table.
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """ initializes the class attributes*arg is an unused variable"""
        str_fdate = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        # self.created_at = datetime.today()
        # self.updated_at = datetime.today()
        if kwargs is not None and kwargs != {}:
            for k, v in kwargs.items():
                if k == '__class__':
                    continue
                setattr(self, k, v)
                if k == "created_at":
                    self.__dict__[k] = datetime.strptime(v, str_fdate)
                elif k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, str_fdate)
                if k != "__class__":
                    self.__dict__[k] = v
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            # models.storage.new(self)

    def __str__(self):
        """ string representation of the BaseModel intance """
        clName = type(self).__name__
        d = self.__dict__
        str = "[{}] ({}) {}".format(clName, self.id, d)
        return str

    def save(self):
        """ updates the instance attribute update_at """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict_db(self):
        """return all keys and values of the objectinstance from __dict__"""
        dictcopy = self.__dict__.copy()
        if type(self.created_at) is str:
            pass
            # dictcopy["created_at"] = self.created_at
        else:
            dictcopy["created_at"] = self.created_at.isoformat()
        if type(self.updated_at) is str:
            pass
            # dictcopy["updated_at"] = self.updated_at
        else:
            dictcopy["updated_at"] = self.updated_at.isoformat()

        if '_sa_instance_state' in dictcopy.keys():
            del dictcopy['_sa_instance_state']
        return dictcopy

    def to_dict(self, save_fs=None):
        """return all keys and values of the objectinstance from __dict__"""
        dictcopy = self.__dict__.copy()
        if type(self.created_at) is str:
            pass
            # dictcopy["created_at"] = self.created_at
        else:
            dictcopy["created_at"] = self.created_at.isoformat()
        if type(self.updated_at) is str:
            pass
            # dictcopy["updated_at"] = self.updated_at
        else:
            dictcopy["updated_at"] = self.updated_at.isoformat()
        dictcopy["__class__"] = self.__class__.__name__
        if '_password' in dictcopy:
            dictcopy['password'] = dictcopy['_password']
            dictcopy.pop('_password', None)
        if '_sa_instance_state' in dictcopy.keys():
            del dictcopy['_sa_instance_state']
        if save_fs is None:
            if "password" in dictcopy:
                del dictcopy["password"]
        return dictcopy

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
