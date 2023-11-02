#!/usr/bin/python3
# Write a Fabric script that generates a
# .tgz archive from the contents of the web_static
import os
from datetime import *
from fabric.api import *
from fabric import *


def do_pack():
    """Write a Fabric script that generates a .tgz archive
    from the contents of the web_static"""
    dt = datetime.utcnow()
    filename = f"versions/web_static_{dt.year}{dt.month}{dt.day}"\
        f"{dt.hour}{dt.minute}{dt.second}.tgz"
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(filename)).failed is True:
        return None
    return filename
