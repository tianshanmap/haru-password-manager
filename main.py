import os

from fastapi import FastAPI
from services import ServiceManager
from models.web import PasswordItem, AppointmentItem
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db.PasswordDataManager import singleton_config
from db.AppointmentManager import singleton_appointment
from utils.encryption import *
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, FastAPI
import utils.files
app = FastAPI()
router = APIRouter()
# 2. Create a router and set your prefix here
app.include_router(router, prefix="/api/data-manager")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Automatically responds to OPTIONS requests for these methods
    allow_headers=["*"],
)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT")
POSTGRESQL_DB = os.getenv("POSTGRESQL_DB")

singleton_config.start(POSTGRESQL_HOST,POSTGRESQL_USER,POSTGRESQL_PASSWORD,POSTGRESQL_DB,POSTGRESQL_PORT)
singleton_appointment.start(POSTGRESQL_HOST,POSTGRESQL_USER,POSTGRESQL_PASSWORD,POSTGRESQL_DB,POSTGRESQL_PORT)

key = get_secret()
print("secret_key=")
print(key)
item = "are you happy today ?"
encrypted_string = encrypt_string(key, item)
print("encrypted_string=")
print(encrypted_string)
decrypted_string = decrypt_string(key, encrypted_string)
print("decrypted_string=")
print(decrypted_string)


def createResponse(content,contentType="application/json"):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": contentType,
        "Allow": "POST,GET,PUT,DELETE,OPTIONS",
    }
    return JSONResponse(content=content, headers=headers)


@router.post("/password/create")
async def create_password(item: PasswordItem):
    print("Create Password")
    # Convert Pydantic model to a standard dictionary
    item_dict = item.model_dump()
    print(item_dict)
    ServiceManager.create_user(item_dict)
    return createResponse(ServiceManager.list_users())

@router.post("/password/update")
async def update_password(item: PasswordItem):
    print("Update Password")
    # Convert Pydantic model to a standard dictionary
    item_dict = item.model_dump()
    print(item_dict)
    ServiceManager.update_user(item_dict)
    return createResponse(ServiceManager.list_users())

@router.get("/password/list")
async def list_password():
    return createResponse(ServiceManager.list_users())

@router.get("/password/purge/{key}")
async def delete_password(key: str):
    print("Delete Password")
    ServiceManager.delete_user(key)
    return createResponse(ServiceManager.list_users())

@router.get("/password/backup")
async def backup_password():
    ServiceManager.backup()
    return createResponse(ServiceManager.list_users())

@router.get("/password/export")
async def export_password():
    password = ServiceManager.export_password()
    password = encrypt_string(get_secret(), password)
    target_file = utils.files.write_export_file("export","export.txt", password)
    # Set headers to force download and name the file
    headers = {
        "Content-Disposition": f"attachment; filename=password.txt"
    }

    # Return StreamingResponse with the chunk generator
    return StreamingResponse(
        utils.files.file_chunk_generator(target_file),
        headers=headers,
        media_type="application/octet-stream"
    )

@router.post("/password/import")
async def import_file(file: UploadFile = File(...)):
    # Optional: Validate file extensions/types
    print(file.content_type)
    if file.content_type not in ["text/plain"]:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    destination = UPLOAD_DIR / file.filename

    # Read and save file in chunks to minimize memory overhead
    with open(destination, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):  # 1MB chunks
            buffer.write(chunk)
    content = utils.files.read_file(destination)
    decrypted_string = decrypt_string(get_secret(), content)
    ServiceManager.import_password(decrypted_string)
    return createResponse(ServiceManager.list_users())

@router.post("/appointment/create")
async def create_appointment(item: AppointmentItem):
    print("Create appointment started")
    # Convert Pydantic model to a standard dictionary
    item_dict = item.model_dump()
    print("create_appointment,item_dict=",item_dict)
    ServiceManager.create_appointment(item_dict)
    return createResponse(ServiceManager.list_appointment_by_date(item_dict["name"],item_dict["start_date"]))

@router.post("/appointment/update")
async def update_appointment(item: AppointmentItem):
    print("update_appointment-web")
    # Convert Pydantic model to a standard dictionary
    item_dict = item.model_dump()
    ServiceManager.update_appointment(item_dict)
    return createResponse(ServiceManager.list_appointment_by_date(item_dict["name"],item_dict["start_date"]))

@router.get("/appointment/list/{name}/{start_date}")
async def list_appointment(name,start_date):
    return createResponse(ServiceManager.list_appointment_by_date(name,start_date))

@router.get("/appointment/list-month/{name}/{start_month}")
async def list_appointment_by_month(name,start_month):
    return createResponse(ServiceManager.list_appointment_by_month(name,start_month))

@router.get("/appointment/delete/{name}/{start_date}")
async def delete_appointment_by_date(name,start_date):
    print("Delete appointment by date")
    ServiceManager.delete_appointment_by_date(name,start_date)
    return createResponse(ServiceManager.list_appointment_by_date(name,start_date))

@router.get("/appointment/delete/{name}/{start_date}/{start_time}")
async def delete_appointment_by_datetime(name,start_date,start_time):
    print("Delete appointment by date")
    ServiceManager.delete_appointment_by_datetime(name,start_date,start_time)
    return createResponse(ServiceManager.list_appointment_by_date(name,start_date))
