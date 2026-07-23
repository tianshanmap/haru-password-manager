import json
from models.service import *
from utils.files import *
from db.PasswordDataManager import singleton_config

ENTIRY_FILE_PATH = "./data/entities.json"
def create_user(item) -> str:
    singleton_config.add_password(item["key"],item["username"],item["password"],item["description"])
    return f"Hello, {item["username"]}!"
def update_user(item) -> str:
    singleton_config.update_password(item["key"],item["username"],item["password"],item["description"])
    return f"Hello, {item["username"]}!"
def delete_user(key: str):
    singleton_config.delete_password(key)
def list_users():
    return singleton_config.retrieve_all_passwords()
def get_user(key: str):
    list_of_entiry = list_users()
    for entity in list_of_entiry:
        if entity["key"] == key:
            return entity;
