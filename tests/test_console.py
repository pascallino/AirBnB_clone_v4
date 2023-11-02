#!/usr/bin/python3
""" unit test for the HBNB Console

unittest class:
    TestHBNBCommand_prompting
    """
import sys
import os
from os import getenv
import unittest
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch
from models import storage
from models.engine.file_storage import FileStorage


class TestHBNBCommand_prompt(unittest.TestCase):
    """ testing the prompt for the interpreter """

    def test_prompt_string(self):
        """ test prompt string """
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_emptyline(self):
        """ test empty line """
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd(''))
            self.assertEqual("", out.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """ testing quit for the interpreter """

    def test_help_quit(self):
        quit = r"Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help quit'))
            self.assertEqual(quit, out.getvalue().strip())

    def test_help_EOF(self):
        eof = "End of File"
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help EOF'))
            self.assertEqual(eof, out.getvalue().strip())

    def test_help_destroy(self):
        des = "Deletes an object from file.json"
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help destroy'))
            self.assertEqual(des, out.getvalue().strip())

    def test_help_show(self):
        sh = """Prints the string representation of an \
                instance based on the class name and id"""
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help show'))
            self.assertEqual(sh, out.getvalue().strip())

    def test_help_all(self):
        all = """<class name>.all(), all, all <class name>"""
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help all'))
            self.assertEqual(all, out.getvalue().strip())

    def test_help_update(self):
        upt = """Usage: update <class name> <id>
        <attribute name> "<attribute value>"""
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help update'))
            self.assertEqual(upt, out.getvalue().strip())

    def test_help_create(self):
        ct = """Ex: $ create User/State create an object class with an id"""
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help create'))
            self.assertEqual(ct, out.getvalue().strip())

    def test_help_count(self):
        cnt = """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help count'))
            self.assertEqual(cnt, out.getvalue().strip())

    def test_help_help(self):
        help = "List available commands with \"help\" "\
                "or detailed help with \"help cmd\"."
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertFalse(HBNBCommand().onecmd('help help'))
            self.assertEqual(help, out.getvalue().strip())

    def test_help(self):
        help = ("Documented commands (type help <topic>):\n"
                "========================================\n"
                "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(help, output.getvalue().strip())


class TestHBNBCommand_quit(unittest.TestCase):
    """ Test EOF and quit for the cmd interpreter """

    def test_EOF(self):
        """ End of file test """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_quit(self):
        """ quit the program """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))


class TestHBNBCommand_create(unittest.TestCase):
    """ test for create command and output """

    @classmethod
    def setUp(self):
        """ before the test begin call the setUp method"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """ After test complet call the tearDown method """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_create_missing_class_name_error(self):
        """ test for missing class name"""
        errormsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_create_wrong_class(self):
        """ test for invalid class """
        errormsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Pascal"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_create_wrong_command(self):
        """ test for wrong command"""
        errormsg = "*** Unknown syntax: classes"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("classes"))
            self.assertEqual(errormsg, output.getvalue().strip())
        errormsg = "*** Unknown syntax: BaseModel2"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel2"))
            self.assertEqual(errormsg, output.getvalue().strip())


class TestHBNBCommand_show(unittest.TestCase):
    """ test for show command and output """

    @classmethod
    def setUp(self):
        """ before the test begin call the setUp method"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """ After test complet call the tearDown method """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_show_missing_class_name_error(self):
        """ test for missing class name """
        errormsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_show_wrong_class(self):
        """ test for class existence """
        errormsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show basemodel"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("basemodel.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_show_missing_id(self):
        """ test for no instance id"""
        errormsg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_show_missing_id_within_brackets(self):
        """ test <class name>.show(id) if id is missing """
        errormsg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_show_output_for_objects_dict(self):
        """ test show for new objects created """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            bmID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(bmID)]
            command = "show BaseModel {}".format(bmID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            RvID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(RvID)]
            command = "show Review {}".format(RvID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            stateID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(stateID)]
            command = "show State {}".format(stateID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            UID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(UID)]
            command = "show User {}".format(UID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            AmdID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(AmdID)]
            command = "show Amenity {}".format(AmdID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            PlaceID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(PlaceID)]
            command = "show Place {}".format(PlaceID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            CityID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(CityID)]
            command = "show City {}".format(CityID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_show_no_instance_found_in_parenthesis(self):
        """ test for instance found in show parenthesis """
        errormsg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(7979)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(6864)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(9089)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(1467)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(3421)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show(9453)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show(23129)"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_show_no_instance_found(self):
        """ test no instance found for show method """
        errormsg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1876867567"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 908787"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 5755453"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 0997656"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 357668"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place 796564"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review 966567"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_show_output_for_objects_keys_InParenthesis(self):
        """ test show.(id) output """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            bmID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(bmID)]
            command = "BaseModel.show({})".format(bmID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            UID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(UID)]
            command = "User.show({})".format(UID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            stateID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(stateID)]
            command = "State.show({})".format(stateID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            RvID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(RvID)]
            command = "Review.show({})".format(RvID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            CityID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(CityID)]
            command = "City.show({})".format(CityID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            PID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(PID)]
            command = "Place.show({})".format(PID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            AmdID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(AmdID)]
            command = "Amenity.show({})".format(AmdID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    """Destroy command test cases """
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass


class TestHBNBCommand_all(unittest.TestCase):
    """ all command test cases """
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_all_class_doesnt_exit(self):
        """ test class doent exist for all <class name> """
        errormsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Pascal"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Pascal.all()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_all_specific_class_display(self):
        """test specific class display using all <class name>"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_all_objects_withoutclass_withparenthesis(self):
        """ test display of all objet Usage .all()"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_all_objects_display(self):
        """ test for all objects display """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_all_specific_class_display_with_all_parenthesis(self):
        """ test <class name>.all()  if output is correct"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())


class TestHBNBCommand_count(unittest.TestCase):
    """Unittest to count if the objects saved are matching with
    whats in the json file"""

    @classmethod
    def setUp(self):
        """ set up the enviromants """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        """ teardown the enviroments """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_count_wrong_class(self):
        """ count from an invaluid calss """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("pascal.count()"))
            self.assertEqual("0", output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_count_specific_object(self):
        """ count specific objects if same"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", output.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """ test update for object keys/value pair """
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_update_intance_id_is_missing_in_parenthesis(self):
        """test update intance id is missing in parenthesis"""
        errormsg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_update_intance_id_is_missing(self):
        """ test instance id is missing """
        errormsg = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_update_for_missing_class(self):
        """test missing class for update commad """
        errormsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_update_no_instance_found_in_parenthesis(self):
        errormsg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(889897)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update(7891)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update(1835)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update(1909)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(yu1)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update(jiji)"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update(lplp1)"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_update_class_doesnt_exist(self):
        """test class doesnt exist for update commad """
        errormsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update pascal"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("pascal.update()"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_update_no_instance_found_no_parenthesis(self):
        """ test_update_no_instance_found_no_parenthesis """
        errormsg = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel huuj"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User hidd"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State khikhk"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City fgfcbvf"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity yfvvb"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place 65gg"))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review lolo"))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_command_for_missing_attribute_name_in_parenthesis(self):
        """test_update_command_for_missing_attribute_name_in_parenthesis"""
        errormsg = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            bmId = output.getvalue().strip()
            Cmd = "BaseModel.update({})".format(bmId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            UId = output.getvalue().strip()
            Cmd = "User.update({})".format(UId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            stateId = output.getvalue().strip()
            Cmd = "State.update({})".format(stateId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            CityId = output.getvalue().strip()
            Cmd = "City.update({})".format(CityId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            AmdId = output.getvalue().strip()
            Cmd = "Amenity.update({})".format(AmdId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            placeId = output.getvalue().strip()
            Cmd = "Place.update({})".format(placeId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            placeId = output.getvalue().strip()
            Cmd = "Review.update({})".format(placeId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_command_for_missing_attribute_name(self):
        """test_update_command_for_missing_attribute_name"""
        errormsg = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            RvId = output.getvalue().strip()
            Cmd = "update Review {}".format(RvId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            stateId = output.getvalue().strip()
            testCmd = "update State {}".format(stateId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            CityId = output.getvalue().strip()
            testCmd = "update City {}".format(CityId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            AmdId = output.getvalue().strip()
            Cmd = "update Amenity {}".format(AmdId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            PlaceId = output.getvalue().strip()
            Cmd = "update Place {}".format(PlaceId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            UserId = output.getvalue().strip()
            Cmd = "update User {}".format(UserId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
            errormsg = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            bmId = output.getvalue().strip()
            Cmd = "update BaseModel {}".format(bmId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_for_missing_attr_value(self):
        """ test update command for missing attr
        value without the parenthesis"""
        errormsg = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            bmId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "update BaseModel {} attr_name".format(bmId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            UId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "update User {} attr_name".format(UId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            stateId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "update State {} attr_name".format(stateId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            CityId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "update City {} attr_name".format(CityId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            AmdId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "update Amenity {} attr_name".format(AmdId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            PlaceId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "update Place {} attr_name".format(PlaceId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            RvId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "update Review {} attr_name".format(RvId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_for_missing_attr_value_in_parenthesis(self):
        """test_update_for_missing_attr_value_in_parenthesis """
        errormsg = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            bmId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "BaseModel.update({}, age)".format(bmId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            UId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "User.update({}, fname)".format(UId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            stateId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "State.update({}, sname)".format(stateId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            CityId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "City.update({}, City_name)".format(CityId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            AmdId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "Amenity.update({}, Type)".format(AmdId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            PlaceId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "Place.update({}, country)".format(PlaceId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            RvId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            Cmd = "Review.update({}, review)".format(RvId)
            self.assertFalse(HBNBCommand().onecmd(Cmd))
            self.assertEqual(errormsg, output.getvalue().strip())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_if_value_are_same(self):
        """ test_update_if_value_are_same """
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            bmId = output.getvalue().strip()
        Cmd = "update BaseModel {} first_name 'pascal'".format(bmId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["BaseModel.{}".format(bmId)]
        self.assertEqual("pascal", test_dict.__dict__["first_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            stateId = output.getvalue().strip()
        Cmd = "update State {} State_name 'Lagos'".format(stateId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["State.{}".format(stateId)]
        self.assertEqual("Lagos", test_dict.__dict__["State_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            PlaceId = output.getvalue().strip()
        Cmd = "update Place {} placeid 89".format(PlaceId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["Place.{}".format(PlaceId)]
        self.assertEqual("89", test_dict.__dict__["placeid"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            UId = output.getvalue().strip()
        Cmd = "update User {} name ojukwu".format(UId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["User.{}".format(UId)]
        self.assertEqual("ojukwu", test_dict.__dict__["name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            CityId = output.getvalue().strip()
        Cmd = "update City {} name 'abj'".format(CityId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["City.{}".format(CityId)]
        self.assertEqual("abj", test_dict.__dict__["name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            AmdId = output.getvalue().strip()
        Cmd = "update Amenity {} asset house".format(AmdId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["Amenity.{}".format(AmdId)]
        self.assertEqual("house", test_dict.__dict__["asset"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            AmdId = output.getvalue().strip()
        Cmd = "update Review {} text house".format(AmdId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["Review.{}".format(AmdId)]
        self.assertEqual("house", test_dict.__dict__["text"])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_if_value_are_same_parenthesis(self):
        """ test_update_if_value_are_same_parenthesis """
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            bmId = output.getvalue().strip()
        Cmd = "BaseModel.update({}, first_name, 'pascal')".format(bmId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["BaseModel.{}".format(bmId)]
        self.assertEqual("pascal", test_dict.__dict__["first_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            stateId = output.getvalue().strip()
        Cmd = "State.update({}, State_name, 'Lagos')".format(stateId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["State.{}".format(stateId)]
        self.assertEqual("Lagos", test_dict.__dict__["State_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            PlaceId = output.getvalue().strip()
        Cmd = "Place.update({}, placeid, '89')".format(PlaceId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["Place.{}".format(PlaceId)]
        self.assertEqual("89", test_dict.__dict__["placeid"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            UId = output.getvalue().strip()
        Cmd = "User.update({}, name, ojukwu)".format(UId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["User.{}".format(UId)]
        self.assertEqual("ojukwu", test_dict.__dict__["name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            CityId = output.getvalue().strip()
        Cmd = "City.update({}, name, 'abj')".format(CityId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["City.{}".format(CityId)]
        self.assertEqual("abj", test_dict.__dict__["name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            AmdId = output.getvalue().strip()
        Cmd = "Amenity.update({}, asset, house)".format(AmdId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["Amenity.{}".format(AmdId)]
        self.assertEqual("house", test_dict.__dict__["asset"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            AmdId = output.getvalue().strip()
        Cmd = "Review.update({}, text, house)".format(AmdId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["Review.{}".format(AmdId)]
        self.assertEqual("house", test_dict.__dict__["text"])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_dictionary_key_and_value_pair(self):
        """test_update_dictionary_key_and_value_pair"""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            bmId = output.getvalue().strip()
        Cmd = "update BaseModel {} ".format(bmId)
        Cmd += "{'f_name': 'f_value'}"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["BaseModel.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            bmId = output.getvalue().strip()
        Cmd = "update User {} ".format(bmId)
        Cmd += "{'f_name': 'f_value'}"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["User.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            bmId = output.getvalue().strip()
        Cmd = "update Review {} ".format(bmId)
        Cmd += "{'f_name': 'f_value'}"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["Review.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            bmId = output.getvalue().strip()
        Cmd = "update City {} ".format(bmId)
        Cmd += "{'f_name': 'f_value'}"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["City.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            bmId = output.getvalue().strip()
        Cmd = "update Place {} ".format(bmId)
        Cmd += "{'f_name': 'f_value'}"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["Place.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            bmId = output.getvalue().strip()
        Cmd = "update Amenity {} ".format(bmId)
        Cmd += "{'f_name': 'f_value'}"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["Amenity.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            bmId = output.getvalue().strip()
        Cmd = "update State {} ".format(bmId)
        Cmd += "{'f_name': 'f_value'}"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["State.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_dictionary_key_and_value_pair_in_parenthesis(self):
        """test_update_dictionary_key_and_value_pair_in_parenthesis"""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            bmId = output.getvalue().strip()
        Cmd = "BaseModel.update({}, ".format(bmId)
        Cmd += "{'f_name': 'f_value'})"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["BaseModel.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            bmId = output.getvalue().strip()
        Cmd = "User.update({}, ".format(bmId)
        Cmd += "{'f_name': 'f_value'})"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["User.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            bmId = output.getvalue().strip()
        Cmd = "Review.update({}, ".format(bmId)
        Cmd += "{'f_name': 'f_value'})"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["Review.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            bmId = output.getvalue().strip()
        Cmd = "Place.update({}, ".format(bmId)
        Cmd += "{'f_name': 'f_value'})"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["Place.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            bmId = output.getvalue().strip()
        Cmd = "City.update({}, ".format(bmId)
        Cmd += "{'f_name': 'f_value'})"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["City.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            bmId = output.getvalue().strip()
        Cmd = "Amenity.update({}, ".format(bmId)
        Cmd += "{'f_name': 'f_value'})"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["Amenity.{}".format(bmId)].__dict__
        self.assertEqual("f_value", test_dict["f_name"])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_validate_if_integer_attvalue_saves(self):
        """test_update_validate_if_integer_attvalue_saves"""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            PlaceId = output.getvalue().strip()
        Cmd = "update Place {} number_bathrooms 98".format(PlaceId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["Place.{}".format(PlaceId)].__dict__
        self.assertEqual(98, test_dict["number_bathrooms"])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_validate_if_integer_attvalue_saves_parenthesis(self):
        """test_update_validate_if_integer_attvalue_saves_parenthesis"""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            PlaceId = output.getvalue().strip()
        Cmd = "Place.update({}, max_guest, 198)".format(PlaceId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["Place.{}".format(PlaceId)].__dict__
        self.assertEqual(198, test_dict["max_guest"])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_update_validate_if_float_attvalue_saves(self):
        """test_update_validate_if_float_attvalue_saves"""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            PlaceId = output.getvalue().strip()
        Cmd = "update Place {} longitude 9.3".format(PlaceId)
        self.assertFalse(HBNBCommand().onecmd(Cmd))
        test_dict = storage.all()["Place.{}".format(PlaceId)].__dict__
        self.assertEqual(9.3, test_dict["longitude"])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_for_integer_value_in_dictionary_parenthesis(self):
        """test_for_integer_value_in_dictionary_parenthesis"""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            bmId = output.getvalue().strip()
        Cmd = "Place.update({}, ".format(bmId)
        Cmd += "{'max_guest': 290})"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["Place.{}".format(bmId)].__dict__
        self.assertEqual(290, test_dict["max_guest"])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_for_integer_value_in_dictionary(self):
        """test_for_integer_value_in_dictionary"""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            bmId = output.getvalue().strip()
        Cmd = "update Place {} ".format(bmId)
        Cmd += "{'max_guest': 290})"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["Place.{}".format(bmId)].__dict__
        self.assertEqual(290, test_dict["max_guest"])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_for_float_value_in_dictionary(self):
        """test_for_float_value_in_dictionary"""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            bmId = output.getvalue().strip()
        Cmd = "update Place {} ".format(bmId)
        Cmd += "{'longitude': 2.80})"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["Place.{}".format(bmId)].__dict__
        self.assertEqual(2.80, test_dict["longitude"])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'pascal', 'NO DB')
    def test_for_float_value_in_dictionary_parenthesis(self):
        """test_for_float_value_in_dictionary_parenthesis"""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            bmId = output.getvalue().strip()
        Cmd = "Place.update({}, ".format(bmId)
        Cmd += "{'latitude': 2.4})"
        HBNBCommand().onecmd(Cmd)
        test_dict = storage.all()["Place.{}".format(bmId)].__dict__
        self.assertEqual(2.4, test_dict["latitude"])


if __name__ == '__main__':
    unittest.main()
