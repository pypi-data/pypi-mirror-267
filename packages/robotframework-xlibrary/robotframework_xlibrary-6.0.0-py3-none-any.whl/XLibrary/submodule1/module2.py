#submodule1/module2.py
# -*- coding: utf-8 -*-
from robot.api.deco import keyword
import pymongo
import logging
class XDrint:
    def CDCDCD(self):
        print("Hello, world! เทสภาษาไทย222")

    @keyword("Connect Mongodb With URL")
    def connect_to_mongodb_with_uri(self, dbURI):
        """
        เชื่อมต่อกับ MongoDB โดยใช้ URI ที่ให้มา

        ตัวอย่างการใช้งาน:
        | # เพื่อเชื่อมต่อโดยใช้ MongoDB URI |
        | Connect To MongoDB With URI | mongodb+srv://yourusername:yourpassword@yourhost |
        """
        self._dbconnection = pymongo.MongoClient(dbURI)
        logging.debug("| Connected to MongoDB using URI | %s |" % dbURI)
