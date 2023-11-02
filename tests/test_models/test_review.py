#!/usr/bin/python3
""" unittest for City class """
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.review import Review
from datetime import datetime
import json
import os
from time import sleep
import models
import unittest
from os import getenv


class TestReview_save(unittest.TestCase):
    """ test save method  for Review class """
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
    def test_save_for_review_object(self):
        """ test_save_for_review_object """
        review = Review()
        review.save()
        Rkey = "Review." + review.id
        objs = models.storage.all()
        with open("file.json", "r") as file:
            self.assertIn(Rkey, file.read())
            self.assertIn(Rkey, objs)

    def test_save_and_pass_argument(self):
        """ test_save_and_pass_argument """
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_on_two_calls(self):
        """ test save for two different calls """
        review = Review()
        sleep(0.1)
        updated_at_1 = review.updated_at
        review.save()
        updated_at_2 = review.updated_at
        self.assertLess(updated_at_1, updated_at_2)
        sleep(0.1)
        review.save()
        self.assertLess(updated_at_2, review.updated_at)


class TestReview_to_dict(unittest.TestCase):
    """class to test to_dict method for Review class """
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
        review = Review()
        self.assertNotEqual(review.__dict__, review.to_dict())

    def test_to_dict_type(self):
        """ test_to_dict_type """
        review = Review()
        self.assertTrue(dict, type(review.to_dict()))

    def test_if_to_dict_kv_is_same_with__dict__(self):
        """ check if  test passes the  missing __class__ in __dict__"""
        review = Review()
        self.assertNotEqual(review.to_dict(), review.__dict__)

    def test_if_2_dict_kv_are_equal(self):
        """ test_if_2_dict_kv_are_equal """
        date_now = datetime.today()
        review = Review()
        review.id = "89755"
        review.place_id = "454545"
        review.user_id = "8267"
        review.text = "i am a student of ALX"
        review.created_at = date_now
        review.updated_at = date_now
        dict_review = {
            '__class__': 'Review',
            'id': '89755',
            'place_id': '454545',
            'text': 'i am a student of ALX',
            'created_at': date_now.isoformat(),
            'updated_at': date_now.isoformat(),
            'user_id': '8267'
        }
        self.assertDictEqual(dict_review, review.to_dict())

    def test_dict_attributes_if_equal(self):
        """test_dict_attributes_if_equal"""
        review = Review()
        review.attr_name = "Pascal"
        review.age = 67
        self.assertEqual("Pascal", review.attr_name)
        self.assertIn("attr_name", review.to_dict())


class TestReview___str__(unittest.TestCase):
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


class TestReview__init__(unittest.TestCase):
    """ test init method for Review"""
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

    def test_review_with_none_parameters(self):
        """ test_review_with_none_parameters"""
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_superclass_of_review(self):
        """ test_superclass_of_review """
        review = Review()
        self.assertTrue(issubclass(type(review), BaseModel))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_name_is_public_class_attribute(self):
        """ check if attr type is same as dict as well"""
        review = Review()
        self.assertIn("user_id", dir(Review()))
        self.assertEqual(str, type(Review.place_id))
        self.assertEqual(str, type(Review.user_id))
        self.assertNotIn("user_id", review.__dict__)

    def test_Review_type(self):
        """ test Review type """
        self.assertEqual(type(Review()), Review)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_Review_public_attributes_type(self):
        """ test_public_public_attributes_type """
        self.assertEqual(str, type(Review.user_id))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_id_if_typeis_str(self):
        """ test_id_if_typeis_str"""
        self.assertEqual(str, type(Review().user_id))

    def test_created_at_if_typeis_datetime(self):
        """ test_created_at_if_type_datetime """
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_if_typeis_datetime(self):
        """ test_updated_at_if_type_datetime """
        self.assertEqual(datetime, type(Review().updated_at))

    def test_dir(self):
        """ test dir and name attr"""
        review = Review()
        review.text = "africa"
        self.assertIn("text", dir(Review()))
        self.assertIn("text", review.__dict__)

    def test_two_review_id_if_they_are_not_same(self):
        """ test_two_review_id_if_they_are_not_same """
        review = Review()
        review_1 = Review()
        self.assertNotEqual(review.id, review_1.id)

    def test_Review_type(self):
        """ test Review type"""
        self.assertEqual(type(Review()), Review)


if __name__ == "__main__":
    unittest.main()
