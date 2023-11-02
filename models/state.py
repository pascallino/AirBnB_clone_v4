#!/usr/bin/python3
"""  class state that inherits from BaseModel:"""
import os
import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import *
from sqlalchemy.orm import *


class State(BaseModel, Base):
    """State attributes for class State"""
    __tablename__ = "states"
    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        name = ""
    else:
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")

    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            """getter attribute cities that returns the list
              of City instances with state_id equals to the
              current State.id"""
            cities_list = []
            for city in models.storage.all('City').values():
                # if City.state_id == State.id:
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
