#!/usr/bin/python3
""" unittest for City class """
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.city import City
from datetime import datetime
import json
import os
from time import sleep
import models
import unittest
from os import getenv


class TestCity_save(unittest.TestCase):
    """ test save method for  City class """
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
    def test_save_for_city_object(self):
        """ test_save_for_city_object """
        city = City()
        city.save()
        Ckey = "City." + city.id
        objs = models.storage.all()
        with open("file.json", "r") as file:
            self.assertIn(Ckey, file.read())
            self.assertIn(Ckey, objs)

    def test_save_and_pass_argument(self):
        """ test_save_and_pass_argument """
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_on_two_calls(self):
        """ test save for two different calls """
        city = City()
        sleep(0.1)
        updated_at_1 = city.updated_at
        city.save()
        updated_at_2 = city.updated_at
        self.assertLess(updated_at_1, updated_at_2)
        sleep(0.1)
        city.save()
        self.assertLess(updated_at_2, city.updated_at)


class TestCity_to_dict(unittest.TestCase):
    """class to test to_dict method for Amenity class """
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
        city = City()
        self.assertNotEqual(city.__dict__, city.to_dict())

    def test_to_dict_type(self):
        """ test_to_dict_type """
        city = City()
        self.assertTrue(dict, type(city.to_dict()))

    def test_if_to_dict_kv_is_same_with__dict__(self):
        """ check if  test passes the  missing __class__ in __dict__"""
        city = City()
        self.assertNotEqual(city.to_dict(), city.__dict__)

    def test_if_2_dict_kv_are_equal(self):
        """ test_if_2_dict_kv_are_equal """
        date_now = datetime.today()
        city = City()
        city.id = "909000"
        city.stateid = "8267"
        city.name = "Lagos"
        city.created_at = date_now
        city.updated_at = date_now
        dict_amenity = {
            '__class__': 'City',
            'id': '909000',
            'name': 'Lagos',
            'created_at': date_now.isoformat(),
            'updated_at': date_now.isoformat(),
            'stateid': '8267'
        }
        self.assertDictEqual(dict_amenity, city.to_dict())

    def test_dict_attributes_if_equal(self):
        """test_dict_attributes_if_equal"""
        city = City()
        city.attr_name = "Pascal"
        city.age = 67
        self.assertEqual("Pascal", city.attr_name)
        self.assertIn("attr_name", city.to_dict())


class TestCity___str__(unittest.TestCase):
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


class TestCity__init__(unittest.TestCase):
    """ test init method for Amenity"""
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

    def test_city_with_none_parameters(self):
        """ test_Amenity_with_none_parameters"""
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_superclass_of_city(self):
        """ test_superclass_of_city """
        city = City()
        self.assertTrue(issubclass(type(city), BaseModel))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_name_is_public_class_attribute(self):
        """ check if attr type is same as dict as well"""
        city = City()
        self.assertIn("name", dir(City()))
        self.assertEqual(str, type(City.state_id))
        self.assertEqual(str, type(City.name))
        self.assertNotIn("state_id", city.__dict__)

    def test_City_type(self):
        """ test City type """
        self.assertEqual(type(City()), City)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_City_public_attributes_type(self):
        """ test_public_public_attributes_type """
        self.assertEqual(str, type(City.name))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_id_if_typeis_str(self):
        """ test_id_if_typeis_str"""
        self.assertEqual(str, type(City().name))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_created_at_if_typeis_datetime(self):
        """ test_created_at_if_type_datetime """
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_if_typeis_datetime(self):
        """ test_updated_at_if_type_datetime """
        self.assertEqual(datetime, type(City().updated_at))

    def test_dir(self):
        """ test dir and name attr"""
        city = City()
        city.name = "africa"
        self.assertIn("name", dir(City()))
        self.assertIn("name", city.__dict__)

    def test_two_city_id_if_they_are_not_same(self):
        """ test_two_city_id_if_they_are_not_same """
        city = City()
        city_1 = City()
        self.assertNotEqual(city.id, city_1.id)

    def test_City_type(self):
        """ test City type"""
        self.assertEqual(type(City()), City)


if __name__ == "__main__":
    unittest.main()
