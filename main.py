import csv
import datetime
from typing import Dict, List

class User:
    def __init__(self, user_id: int, name: str, email: str, role: str, password: str):
        self.__user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.__password = password


    def login(self, password: str):
        if password == self.__password:
            print(f"✅ User {self.name} logged in successfully.")
            return True
        else:
            print("❌ Invalid password. Access denied.")
            return False


    def logout(self):
        print(f"🚪 User {self.name} has logged out.")


    def get_user_id(self):
        return self.__user_id
   
    def get_password(self):
        return self.__password


    @classmethod
    def register(cls, user_id, username, name, email, role, password, users_db):
        if role == "Resident":
            user = Resident(user_id, name, email, password)
        elif role == "Administrator":
            user = Administrator(user_id, name, email, password)
        elif role == "Authority":
            user = Authority(user_id, name, email, password)
        else:
            return None


        users_db[username] = user
        CSVManager.save_users(users_db)


        return user
     

