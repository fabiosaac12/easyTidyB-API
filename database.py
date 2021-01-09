# IMPORTS
import os
import mysql.connector as mariadb
from helpers.functions import *

class SQL:
    # to set the database values
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    # to connect to the database
    def connect(self):
        self.connection = mariadb.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        self.cursor = self.connection.cursor()

    # to execute a query
    def run(self, query, fetch=True, close=True):
        result = False
        try:
            self.cursor.execute(query)
        except:
            try:
                self.connect()
            except:
                return {"message": "Database error"}
            try:
                self.cursor.execute(query)
            except mariadb.errors.DataError:
                result = {"message": "Data too long"}
            except mariadb.errors.IntegrityError as e:
                try:
                    repeatedName = str(e).split("'")[1].split('-')[0]
                    result = {"message": "Repeated data", "id": False, "name": repeatedName}
                except IndexError:
                    print(e)
            except Exception as e:
                print(e)
                result = {"message": "Database error"}
        if fetch == True and not result:
            try:
                result = self.cursor.fetchall()
                result = toJSON(self.cursor, result)
            except Exception as e:
                print(e)
                result = {"message": "Database error"}
        elif not result:
            result = {"message": "good"}
            try:
                result['id'] = self.cursor.lastrowid
            except:
                pass
        try:
            self.connection.commit()
        except Exception as e:
            result = {"message": "Database Error"}
            print(e)
        if close == True:
            try:
                self.close()
            except:
                result = {"message": "Database error"}
        return result
    
    # to close the database
    def close(self):
        self.cursor.close()
        self.connection.close()

            
sql = SQL(os.environ["DB_HOST"], os.environ["DB_PORT"], os.environ["DB_USER"], os.environ["DB_PW"], os.environ["DB_DB"])
