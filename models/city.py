#!/usr/bin/python3
"""  class City that inherits from BaseModel:"""
from models.base_model import BaseModel, Base
from sqlalchemy import *
from sqlalchemy.orm import *
import os


class City(BaseModel, Base):
    """state_id: string - empty string
    it will be the State.id
    name: string - empty string"""
    __tablename__ = "cities"
    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        state_id = ""
        name = ""
    else:
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        places = relationship("Place", backref="cities", cascade="delete")
