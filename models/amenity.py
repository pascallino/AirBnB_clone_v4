#!/usr/bin/python3
"""  class Amenity that inherits from BaseModel:"""
from models.base_model import BaseModel, Base
from sqlalchemy import *
from sqlalchemy.orm import *
import os


class Amenity(BaseModel, Base):
    """Public class attributes
    name: string - empty string"""
    __tablename__ = "amenities"
    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        name = ""
    else:
        from models.place import place_amenity
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary=place_amenity)
