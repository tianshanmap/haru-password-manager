import json
from models.service import *
from utils.files import *
from db.PasswordDataManager import singleton_config

ENTIRY_FILE_PATH = "./data/entities.json"
def create_user(item) -> str:
    print("item=",item,type(item))
    print("key=",item["key"])
    userPassword = UserPassword(item["key"],item["username"],item["password"],item["description"])
    if exists(ENTIRY_FILE_PATH):
        jsonString = read_file(ENTIRY_FILE_PATH)
        list_of_entiry = json.loads(jsonString)
        found = False
        for entity in list_of_entiry:
            if entity["key"] == item["key"]:
                entity["username"] = item["username"]
                entity["password"] = item["password"]
                entity["description"] = item["description"]
                found = True
                break
        if not found:
            list_of_entiry.append(userPassword.__dict__)
        updated_json = json.dumps(list_of_entiry)
        write_file(ENTIRY_FILE_PATH,updated_json)
    else:
        list_of_entiry = [userPassword.__dict__]
        updated_json = json.dumps(list_of_entiry)
        write_file(ENTIRY_FILE_PATH,updated_json)

    return f"Hello, {item["username"]}!"

def update_user(item) -> str:
    print("item=",item,type(item))

def delete_user(key: str):
    print("key=",key,type(key))
    jsonString = read_file(ENTIRY_FILE_PATH)
    list_of_entiry = json.loads(jsonString)
    updated_list = list(filter(lambda x: x["key"] != key, list_of_entiry))
    write_file(ENTIRY_FILE_PATH, json.dumps(updated_list))
def list_users():
    print("list_users")
    jsonString = read_file(ENTIRY_FILE_PATH)
    return json.loads(jsonString)
def get_user(key: str):
    list_of_entiry = list_users()
    for entity in list_of_entiry:
        if entity["key"] == key:
            return entity