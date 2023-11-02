#!/usr/bin/python3
""" unit test for Based Modelunittest class:Base Model Class"""
from time import sleep
from os import getenv
import sys
import os
import unittest
from models.base_model import BaseModel
from datetime import datetime
from models.engine.file_storage import FileStorage
import time
import uuid
import models
import json


class TestBaseModel___init__(unittest.TestCase):
    """ testing the BaseModel  ___init___ method """

    def test_no_arg_init(self):
        """ test for no arguements """
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_BaseModel_id(self):
        """ test for BaseMOdel id """
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_typeof_datetime(self):
        """ test the type for the created_at """
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_typeof_datetime(self):
        """ test the type for the updated_at """
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_instanceid_are_different(self):
        """ test two id's of two instances """
        Base1 = BaseModel()
        Base2 = BaseModel()
        self.assertNotEqual(Base1.id, Base2.id)

    def test_different_instantiation(self):
        """Tests instantiation of BaseModel class."""

        b = BaseModel()
        self.assertEqual(str(type(b)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(b, BaseModel)
        self.assertTrue(issubclass(type(b), BaseModel))

    def test_different_updated_at(self):
        """ Test for two different dates """
        base1 = BaseModel()
        sleep(0.10)
        base2 = BaseModel()
        self.assertLess(base1.updated_at, base2.updated_at)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_different_created_at(self):
        """ Test for two different dates """
        base1 = BaseModel()
        sleep(0.10)
        base2 = BaseModel()
        self.assertLess(base1.created_at, base2.created_at)

    def test_for_none_arg(self):
        """ test for None values in keys """
        base1 = BaseModel(None)
        self.assertNotIn(None, base1.__dict__.values())

    def test_dict_keys_values(self):
        """Tests for the to_dict(). """
        base1 = BaseModel()
        base1.name = "Pascal"
        base1.age = 28
        bcopy = base1.to_dict()
        self.assertEqual(bcopy["id"], base1.id)
        self.assertEqual(bcopy["__class__"], type(base1).__name__)
        self.assertEqual(bcopy["created_at"], base1.created_at.isoformat())
        self.assertEqual(bcopy["updated_at"], base1.updated_at.isoformat())
        self.assertEqual(bcopy["name"], base1.name)
        self.assertEqual(bcopy["age"], base1.age)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_kwargs(self):
        """ test kwargs argument to_dict() args """
        dtnow = datetime.today()
        dt_str = dtnow.isoformat()
        bmodel1 = BaseModel(id="123", created_at=dt_str, updated_at=dt_str)
        self.assertEqual(bmodel1.id, "123")
        self.assertEqual(bmodel1.created_at, dtnow)
        self.assertEqual(bmodel1.updated_at, dtnow)

    def test_str_(self):
        """ str representation test """
        dtnow = datetime.today()
        dt_repr = repr(dtnow)
        bmodel1 = BaseModel()
        bmodel1.id = "888888"
        bmodel1.created_at = bmodel1.updated_at = dtnow
        bmodel1str = bmodel1.__str__()
        self.assertIn("[BaseModel] (888888)", bmodel1str)
        self.assertIn("'id': '888888'", bmodel1str)
        self.assertIn("'created_at': " + dt_repr, bmodel1str)
        self.assertIn("'updated_at': " + dt_repr, bmodel1str)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_save_time_diff(self):
        """Test save() method time interval"""
        bmodel1 = BaseModel()
        time.sleep(0.5)
        dtnow = datetime.now()
        bmodel1.save()
        dtdiff = bmodel1.updated_at - dtnow
        self.assertTrue(abs(dtdiff.total_seconds()) < 0.01)

    def test_for_None_kwargs_params(self):
        """ test for none for all key value parameters"""
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for to_dict method from BaseModel class."""

    def test_overidedict_with_inbuiltdict(self):
        """ test bm to_dict() method with_inbuilt __dict__"""
        bmodel = BaseModel()
        self.assertNotEqual(bmodel.to_dict(), bmodel.__dict__)

    def test_two_object_dict(self):
        """test with instantiated **kwargs from custom dictionary."""
        d = {"__class__": "BaseModel",
             "updated_at":
             datetime(2024, 12, 30, 23, 59, 59, 123456).isoformat(),
             "created_at": datetime.now().isoformat(),
             "id": uuid.uuid4(),
             "name": "Pascal",
             "age": 18,
             "CGPA": 3.34}
        o = BaseModel(**d)
        self.assertEqual(o.to_dict(), d)

    def test__int__with_to_dict(self):
        """test to_dict() with **kwargs."""
        model = BaseModel()
        model.name = "julien"
        model.my_number = 30
        my_new_model_json = model.to_dict()
        my_new_model = BaseModel(**my_new_model_json)
        self.assertEqual(my_new_model.to_dict(), model.to_dict())

    def test_to_dict_object_type(self):
        """ test type for two dict objects """
        bmodel = BaseModel()
        self.assertTrue(dict, type(bmodel.to_dict()))

    def test_to_dict_attributes(self):
        """ test to_dict attr are same """
        bmodel = BaseModel()
        bmodel.my_name = "Mr pascal"
        bmodel.my_age = 28
        self.assertIn("my_name", bmodel.to_dict())
        self.assertIn("my_age", bmodel.to_dict())

    def test_to_dict_datetime_params_are_type_str(self):
        """ test date type for created_at & updated_at"""
        bmodel = BaseModel()
        bmodel_dict = bmodel.to_dict()
        self.assertEqual(str, type(bmodel_dict["created_at"]))
        self.assertEqual(str, type(bmodel_dict["updated_at"]))


class TestBaseModel_save(unittest.TestCase):
    """Unittests for save method from BaseModel class."""
    @classmethod
    def setUp(self):
        """ setup the enviroments """
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ teardown the enviroments """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def clearStorage(self):
        """ clear the file contents """
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_if_object_in_file(self):
        """test_save_if_object_in_<file.json>"""
        bmodel = BaseModel()
        bmodel.save()
        bmodelid = "BaseModel." + bmodel.id
        with open("file.json", "r") as file:
            self.assertIn(bmodelid, file.read())

    def test_save_no_args(self):
        """Tests save() with no arguments."""
        self.clearStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.save()
        msg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_save_for_many_args(self):
        """Tests save() with too many arguments."""
        self.clearStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.save(self, 98)
        msg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)


class TestBaseModel___str__(unittest.TestCase):
    """ test string representation for bm"""
    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)


if __name__ == '__main__':
    unittest.main()
