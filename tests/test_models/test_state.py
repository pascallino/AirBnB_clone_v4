#!/usr/bin/python3
""" unittest for City class """
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.state import State
from datetime import datetime
import json
import os
from os import getenv
from time import sleep
import models
import unittest


class TestState_save(unittest.TestCase):
    """ test save method for City class """
    @classmethod
    def setUp(self):
        """setUp the  enviroment for testing"""
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
    def test_save_for_state_object(self):
        """ test_save_for_city_object """
        state = State()
        state.save()
        Ckey = "State." + state.id
        objs = models.storage.all()
        with open("file.json", "r") as file:
            self.assertIn(Ckey, file.read())
            self.assertIn(Ckey, objs)

    def test_save_and_pass_argument(self):
        """ test_save_and_pass_argument """
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_on_two_calls(self):
        """ test save for two different calls """
        state = State()
        sleep(0.1)
        updated_at_1 = state.updated_at
        state.save()
        updated_at_2 = state.updated_at
        self.assertLess(updated_at_1, updated_at_2)
        sleep(0.1)
        state.save()
        self.assertLess(updated_at_2, state.updated_at)


class TestState_to_dict(unittest.TestCase):
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
        state = State()
        self.assertNotEqual(state.__dict__, state.to_dict())

    def test_to_dict_type(self):
        """ test_to_dict_type """
        state = State()
        self.assertTrue(dict, type(state.to_dict()))

    def test_if_to_dict_kv_is_same_with__dict__(self):
        """ check if  test passes the  missing __class__ in __dict__"""
        state = State()
        self.assertNotEqual(state.to_dict(), state.__dict__)

    def test_if_2_dict_kv_are_equal(self):
        """ test_if_2_dict_kv_are_equal """
        date_now = datetime.today()
        state = State()
        state.id = "909000"
        state.name = "Lagos"
        state.created_at = date_now
        state.updated_at = date_now
        dict_state = {
            '__class__': 'State',
            'id': '909000',
            'name': 'Lagos',
            'created_at': date_now.isoformat(),
            'updated_at': date_now.isoformat()
        }
        self.assertDictEqual(dict_state, state.to_dict())

    def test_dict_attributes_if_equal(self):
        """test_dict_attributes_if_equal"""
        state = State()
        state.attr_name = "Pascal"
        state.age = 67
        self.assertEqual("Pascal", state.attr_name)
        self.assertIn("attr_name", state.to_dict())


class TestState___str__(unittest.TestCase):
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


class TestState__init__(unittest.TestCase):
    """ test init method for State"""
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
        """ test_State_with_none_parameters"""
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    def test_superclass_of_state(self):
        """ test_superclass_of_state """
        state = State()
        self.assertTrue(issubclass(type(state), BaseModel))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_name_is_public_class_attribute(self):
        """ check if attr type is same as dict as well"""
        state = State()
        self.assertIn("name", dir(State()))
        self.assertEqual(str, type(State.name))
        self.assertNotIn("name", state.__dict__)

    def test_State_type(self):
        """ test State type """
        self.assertEqual(type(State()), State)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_State_public_attributes_type(self):
        """ test_public_public_attributes_type """
        self.assertEqual(str, type(State.name))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_id_if_typeis_str(self):
        """ test_id_if_typeis_str"""
        self.assertEqual(str, type(State().name))

    def test_created_at_if_typeis_datetime(self):
        """ test_created_at_if_type_datetime """
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_if_typeis_datetime(self):
        """ test_updated_at_if_type_datetime """
        self.assertEqual(datetime, type(State().updated_at))

    def test_dir(self):
        """ test dir and name attr"""
        state = State()
        state.name = "AFR"
        self.assertIn("name", dir(State()))
        self.assertIn("name", state.__dict__)

    def test_two_state_id_if_they_are_not_same(self):
        """ test_two_state_id_if_they_are_not_same """
        state = State()
        state_1 = State()
        self.assertNotEqual(state.id, state_1.id)

    def test_User_type(self):
        """ test State type"""
        self.assertEqual(type(State()), State)


if __name__ == "__main__":
    unittest.main()
