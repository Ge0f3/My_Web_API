from services.extensions import mongodb as mdb
import decimal
import datetime

class MongoManager():
    @staticmethod
    def insert_item(table_name, data):
        try:
            result = mdb[table_name].insert_one(data)
            if result.inserted_id:
                return str(result.inserted_id), None
            else:
                return None, 'Data not inserted'
        except Exception as e:
            return None, e

    @staticmethod
    def find_item(table_name, condition={}):
        try:
            result = mdb[table_name].find_one(condition)
            if result:
                return result, None
            else:
                return None, 'Data not found'
        except Exception as e:
            return None, e

    
    @staticmethod
    def find(table_name, condition={}):
        try:
            result = mdb[table_name].find(condition)
            return list(result), None
        except Exception as e:
            return None, e

    @staticmethod
    def update_item(table_name, condition, updates={}):
        try:
            result = mdb[table_name].update_one(condition, updates)
            if result.matched_count == 1:
                return True, None
            else:
                return None, None
        except Exception as e:
            print(str(e))
            return None, e
