#!/usr/bin/python3
""" The file storage engine where the file will be stored """
import models
import sys
import os
import json
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    """ File Storage class to store the
    to save the obj dict to json string and retrieve
    as Object"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ returns the dictionary objects using json.load """
        if cls is not None:
            cls_dict = {}
            if isinstance(cls, str):
                cls = eval(cls)
            for k, v in self.__objects.items():
                if isinstance(v, cls):
                    cls_dict[k] = v
            return cls_dict
        return self.__objects

    def new(self, obj):
        """ sets in object with key classname.id """
        clName = obj.__class__.__name__
        # key = f"{clName}.{obj.id}"
        key = "{}.{}".format(clName, obj.id)
        self.__objects[key] = obj

    def save(self):
        """ serializes the object into the json file """
        objdict = self.__objects
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            dict = {k: val.to_dict(save_fs=1) for k, val in objdict.items()}
            json.dump(dict, file)

    def reload(self):
        """ deserializes back to python object
        do nothing if the file doesnt exist"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
            pyobj = json.load(file)
            for cl in pyobj.values():
                clName = cl["__class__"]
                del cl["__class__"]
                self.new(eval(clName)(**cl))

    def delete(self, obj=None):
        """ delete an object if it exist"""
        if obj:
            clName = obj.__class__.__name__
            key = "{}.{}".format(clName, obj.id)
            # key = f"{clName}.{obj.id}"
            del self.__objects[key]

    def close(self):
        """ calls reload()"""
        self.reload()

    def get(self, cls, id):
        """ retrieve all objects based on class and id"""
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
        countsall  the number of objects in storage
        """
        count = 0
        classes = [User, State, City, Amenity, Place, Review]
        if cls is None:
            count = 0
            for c in classes:
                count = count + len(models.storage.all(c).values())
        else:
            count = len(models.storage.all(cls).values())
        return count
