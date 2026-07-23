from fastapi import FastAPI
from services import ServiceManager
from models.web import PasswordItem
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db.PasswordDataManager import singleton_config

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Automatically responds to OPTIONS requests for these methods
    allow_headers=["*"],
)
items = singleton_config.retrieve_all_passwords()
print(items)
print(type(items))
# singleton_config.create_table()
# singleton_config.add_password("key001","1","2","3")
# singleton_config.add_password("key002","1","2","3")
# singleton_config.add_password("key003","1","2","3")
# singleton_config.update_password("key001","11","21","31")
# singleton_config.delete_password("key001")
# item = singleton_config.retrieve_password("key002")
# if item != None:
#     print(item)
#     key,username,password,description = item
#     print(password)
# item = singleton_config.retrieve_password("key001")
# print(item)
# singleton_config.add_password("key001","neil","meiyou","test")
# singleton_config.add_password("key002","neil","meiyou","test")

@app.get("/")
def main():
    return {"message": "Hello World"}

def createResponse(content,contentType="application/json"):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": contentType,
        "Allow": "POST,GET,PUT,DELETE,OPTIONS",
    }
    return JSONResponse(content=content, headers=headers)


@app.post("/password/create")
async def create_password(item: PasswordItem):
    print("Create Password")
    # Convert Pydantic model to a standard dictionary
    item_dict = item.model_dump()
    print(item_dict)
    ServiceManager.create_user(item_dict)
    return createResponse(ServiceManager.list_users())

@app.post("/password/update")
async def update_password(item: PasswordItem):
    print("Update Password")
    # Convert Pydantic model to a standard dictionary
    item_dict = item.model_dump()
    print(item_dict)
    ServiceManager.update_user(item_dict)
    return createResponse(ServiceManager.list_users())

@app.get("/password/list")
async def list_password():
    return createResponse(ServiceManager.list_users())

@app.get("/password/purge/{key}")
async def delete_password(key: str):
    print("Delete Password")
    ServiceManager.delete_user(key)
    return createResponse(ServiceManager.list_users())
