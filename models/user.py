#!/usr/bin/python3
"""  class User that inherits from BaseModel:"""
from models.base_model import BaseModel, Base
from sqlalchemy import *
from sqlalchemy.orm import *
import hashlib
import os


class User(BaseModel, Base):
    """Public class attributes:
email: string - empty string
password: string - empty string
first_name: string - empty string
last_name: string - empty string"""

    __tablename__ = "users"
    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        email = ""
        _password = ""
        first_name = ""
        last_name = ""
    else:
        email = Column(String(128), nullable=False)
        _password = Column('password',
                           String(128),
                           nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship("Place", backref="user", cascade="delete")
        reviews = relationship("Review", backref="user", cascade="delete")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        """hashing password values"""
        self._password = hashlib.md5(pwd.encode()).hexdigest()
