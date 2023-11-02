#!/usr/bin/python3
""" unittest for amenity class """
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.amenity import Amenity
from datetime import datetime
import json
import os
from time import sleep
import models
from os import getenv
import unittest


class TestAmenity_save(unittest.TestCase):
    """ test save method  for Amenity class """
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_for_amenity_object(self):
        """ test_save_for_amenity_object """
        amenity = Amenity()
        amenity.save()
        objs = models.storage.all()
        Amkey = "Amenity." + amenity.id
        with open("file.json", "r") as file:
            self.assertIn(Amkey, file.read())
            self.assertIn(Amkey, objs)

    def test_save_and_pass_argument(self):
        """ test_save_and_pass_argument """
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.save(None)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_on_two_calls(self):
        """ test save for two different calls """
        amenity = Amenity()
        sleep(0.1)
        updated_at_1 = amenity.updated_at
        amenity.save()
        updated_at_2 = amenity.updated_at
        self.assertLess(updated_at_1, updated_at_2)
        sleep(0.1)
        amenity.save()
        self.assertLess(updated_at_2, amenity.updated_at)


class TestAmenity_to_dict(unittest.TestCase):
    """class to test to_dict method for Amenity class """
    def test_to_dict_keys_if_same(self):
        """  test_to_dict_keys_if_same """
        amenity = Amenity()
        self.assertIn("created_at", amenity.to_dict())

    def test_to_dict_type(self):
        """ test_to_dict_type """
        amenity = Amenity()
        self.assertTrue(dict, type(amenity.to_dict()))

    def test_if_to_dict_kv_is_same_with__dict__(self):
        """ check if  test passes the  missing __class__ in __dict__"""
        amenity = Amenity()
        self.assertNotEqual(amenity.to_dict(), amenity.__dict__)

    def test_if_2_dict_kv_are_equal(self):
        """ test_if_2_dict_kv_are_equal """
        date_now = datetime.today()
        amenity = Amenity()
        amenity.id = "886600"
        amenity.name = "Home appliances"
        amenity.created_at = date_now
        amenity.updated_at = date_now
        dict_amenity = {
            '__class__': 'Amenity',
            'id': '886600',
            'name': 'Home appliances',
            'created_at': date_now.isoformat(),
            'updated_at': date_now.isoformat(),
        }
        self.assertDictEqual(dict_amenity, amenity.to_dict())

    def test_dict_attributes_if_equal(self):
        """test_dict_attributes_if_equal"""
        amenity = Amenity()
        amenity.attr_name = "Pascal"
        amenity.age = 67
        self.assertEqual("Pascal", amenity.attr_name)
        self.assertIn("attr_name", amenity.to_dict())


class TestAmenity__init__(unittest.TestCase):
    """ test init method for Amenity"""
    def test_Amenity_with_none_parameters(self):
        """ test_Amenity_with_none_parameters"""
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_name_is_public_class_attribute(self):
        """ check if attr type is same as dict as well"""
        amenity = Amenity()
        self.assertIn("name", dir(Amenity()))
        self.assertEqual(str, type(Amenity.name))
        self.assertNotIn("name", amenity.__dict__)

    def test_Amenity_type(self):
        """ test Amenity type """
        self.assertEqual(type(Amenity()), Amenity)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_Amenity_public_attributes_type(self):
        """ test_public_public_attributes_type """
        self.assertEqual(str, type(Amenity.name))

    def test_id_if_typeis_str(self):
        """ test_id_if_typeis_str"""
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_if_typeis_datetime(self):
        """ test_created_at_if_type_datetime """
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_if_typeis_datetime(self):
        """ test_updated_at_if_type_datetime """
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_superclass_of_amenity(self):
        """ test_superclass_of_user """
        amenity = Amenity()
        self.assertTrue(issubclass(type(amenity), BaseModel))

    def test_dir(self):
        """ test dir and name attr"""
        amenity = Amenity()
        amenity.name = "car"
        self.assertIn("name", dir(Amenity()))
        self.assertIn("name", amenity.__dict__)

    def test_two_amenities_id_if_they_are_not_same(self):
        """ test_two_amenities_id_if_they_are_not_same """
        amd = Amenity()
        amd_1 = Amenity()
        self.assertNotEqual(amd.id, amd_1.id)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_storage_type(self):
        """ test storage type"""
        self.assertEqual(type(models.storage), FileStorage)


if __name__ == "__main__":
    unittest.main()
