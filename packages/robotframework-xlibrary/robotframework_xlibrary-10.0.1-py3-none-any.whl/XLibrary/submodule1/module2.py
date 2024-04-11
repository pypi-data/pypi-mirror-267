#submodule1/module2.py
# -*- coding: utf-8 -*-
from robot.api.deco import keyword
import ast
import pymongo
import logging

class XDrint:
    def CDCDCD(self):
        print("Hello, world! เทสภาษาไทย222")

    @keyword("Connect Mongodb With URL")
    def connect_to_mongodb_with_uri(self, dbURI):
        """
        เชื่อมต่อกับ MongoDB โดยใช้ URI 

        ตัวอย่างการใช้งาน:
        |   Connect Mongodb With URL    | mongodb+srv://yourusername:yourpassword@yourhost |
        """
        self._dbconnection = pymongo.MongoClient(dbURI)
        logging.debug("| Connected to MongoDB using URI | %s |" % dbURI)
    
    @keyword("Query MongoDB")
    def query_mongodb(self, database_name, collection_name, query):
        """
        Query ข้อมูลใน MongoDB

        ตัวอย่างการใช้งาน:
        | ${result} =  Query MongoDB  database_name  collection_name  {"productCharacteristic.value": "0934025144"} |
        | Log  ${result} |
        """
        collection = self._dbconnection[database_name][collection_name]
        query_dict = ast.literal_eval(query)
        result = collection.find(query_dict)
        return list(result)