#!/usr/bin/python3
"""  class Review that inherits from BaseModel:"""
from models.base_model import BaseModel, Base
from sqlalchemy import *
from sqlalchemy.orm import *
import os


class Review(BaseModel, Base):
    """Review attributes for class Review"""
    __tablename__ = "reviews"
    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        place_id = ""
        user_id = ""
        text = ""
    else:
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        text = Column(String(1024), nullable=False)
