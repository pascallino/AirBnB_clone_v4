#!/usr/bin/python3
""" unittest for Place class """
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.place import Place
from datetime import datetime
import json
import os
from time import sleep
import models
import unittest
from os import getenv


class TestPlace_save(unittest.TestCase):
    """ test save method for Place  class """
    @classmethod
    def setUp(self):
        """setUp the enviroment for testing"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ teardown the enviroment to end the testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_for_place_object(self):
        """ test_save_for_place_object """
        place = Place()
        place.save()
        Pkey = "Place." + place.id
        objs = models.storage.all()
        with open("file.json", "r") as file:
            self.assertIn(Pkey, file.read())
            self.assertIn(Pkey, objs)

    def test_save_and_pass_argument(self):
        """ test_save_and_pass_argument """
        place = Place()
        with self.assertRaises(TypeError):
            place.save(None)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_on_two_calls(self):
        """ test save for two different calls """
        place = Place()
        sleep(0.1)
        updated_at_1 = place.updated_at
        place.save()
        updated_at_2 = place.updated_at
        self.assertLess(updated_at_1, updated_at_2)
        sleep(0.1)
        place.save()
        self.assertLess(updated_at_2, place.updated_at)


class TestPlace_to_dict(unittest.TestCase):
    """class to test to_dict method for Place class """
    @classmethod
    def setUp(self):
        """ setUp the enviroment for testing"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ teardown the enviroment to end the testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def test_to_dict_keys_if_same(self):
        """  test_to_dict_keys_if_same """
        place = Place()
        self.assertNotEqual(place.__dict__, place.to_dict())

    def test_to_dict_type(self):
        """ test_to_dict_type """
        place = Place()
        self.assertTrue(dict, type(place.to_dict()))

    def test_if_to_dict_kv_is_same_with__dict__(self):
        """ check if  test passes the  missing __class__ in __dict__"""
        place = Place()
        self.assertNotEqual(place.to_dict(), place.__dict__)

    def test_if_2_dict_kv_are_equal(self):
        """ test_if_2_dict_kv_are_equal """
        date_now = datetime.today()
        place = Place()
        place.id = "89755"
        place.city_id = "092"
        place.user_id = "1234"
        place.name = "Alx"
        place.number_rooms = 10
        place.number_bathrooms = 45
        place.max_guest = 18
        place.price_by_night = 150
        place.latitude = 2.4
        place.longitude = 1.3
        place.description = "i am a student of ALX"
        place.created_at = date_now
        place.updated_at = date_now
        dict_place = {
            '__class__': 'Place',
            'id': '89755',
            'name': 'Alx',
            'number_rooms': 10,
            'number_bathrooms': 45,
            'max_guest': 18,
            'price_by_night': 150,
            'latitude': 2.4,
            'longitude': 1.3,
            'description': 'i am a student of ALX',
            'created_at': date_now.isoformat(),
            'updated_at': date_now.isoformat(),
            'city_id': '092',
            'user_id': '1234'
        }
        self.assertDictEqual(dict_place, place.to_dict())

    def test_dict_attributes_if_equal(self):
        """test_dict_attributes_if_equal"""
        place = Place()
        place.attr_name = "Pascal"
        place.age = 67
        self.assertEqual("Pascal", place.attr_name)
        self.assertIn("attr_name", place.to_dict())


class TestPlace___str__(unittest.TestCase):
    @classmethod
    def setUp(self):
        """ setup the enviroment for testing"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ teardown the enviroment to end the testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass


class TestPlace__init__(unittest.TestCase):
    """ test init method for Place"""
    @classmethod
    def setUp(self):
        """ setup the enviroment for testing"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ teardown the enviroment to end the testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def test_place_with_none_parameters(self):
        """ test_place_with_none_parameters"""
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_superclass_of_place(self):
        """ test_superclass_of_place """
        place = Place()
        self.assertTrue(issubclass(type(place), BaseModel))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_name_is_public_class_attribute(self):
        """ check if attr type is same as dict as well"""
        place = Place()
        self.assertIn("max_guest", dir(Place()))
        self.assertEqual(str, type(Place.city_id))
        self.assertEqual(str, type(Place.user_id))
        self.assertNotIn("max_guest", place.__dict__)

    def test_place_type(self):
        """ test Place type to be sure its same """
        self.assertEqual(type(Place()), Place)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_Place_public_attributes_type(self):
        """ test_public_public_attributes_type """
        self.assertEqual(str, type(Place.user_id))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_id_if_typeis_str(self):
        """ test_id_if_typeis_str"""
        self.assertEqual(str, type(Place().user_id))

    def test_created_at_if_typeis_datetime(self):
        """ test_created_at_if_type_datetime """
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_if_typeis_datetime(self):
        """ test_updated_at_if_type_datetime """
        self.assertEqual(datetime, type(Place().updated_at))

    def test_dir(self):
        """ test dir and name attr"""
        place = Place()
        place.description = "africa"
        self.assertIn("description", dir(Place()))
        self.assertIn("description", place.__dict__)

    def test_two_Place_id_if_they_are_not_same(self):
        """ test_two_Place_id_if_they_are_not_same """
        place = Place()
        place_1 = Place()
        self.assertNotEqual(place.id, place_1.id)

    def test_Place_type(self):
        """ test Place type to see if they are they same"""
        self.assertEqual(type(Place()), Place)


if __name__ == "__main__":
    unittest.main()
