from flask_login import UserMixin
from flask import url_for, send_from_directory
from function_db import DataBase

class UserLogin(UserMixin):
    def fromDB(self, user_id):
        dab = DataBase()
        print(user_id, user_id, user_id, user_id)
        self.__user = dab.get_user(int(user_id))
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return self.__user[0]['id']

    def getName(self):
        return self.__user[0]['name'] if self.__user else "NoName"

    def getPhone(self):
        return self.__user[0]['number'] if self.__user else "NoPhone"
    
    def getEmail(self):
        return self.__user[0]['email'] if self.__user else "Without Email"