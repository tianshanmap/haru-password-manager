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
import utils.files
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Automatically responds to OPTIONS requests for these methods
    allow_headers=["*"],
)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
singleton_config.create_table()
singleton_config.create_table_backup()
singleton_appointment.create_table()
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

@app.get("/password/backup")
async def backup_password():
    ServiceManager.backup()
    return createResponse(ServiceManager.list_users())

@app.get("/password/export")
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

@app.post("/password/import")
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

@app.post("/appointment/create")
async def create_appointment(item: AppointmentItem):
    print("Create appointment started")
    # Convert Pydantic model to a standard dictionary
    item_dict = item.model_dump()
    print("create_appointment,item_dict=",item_dict)
    ServiceManager.create_appointment(item_dict)
    return createResponse(ServiceManager.list_appointment_by_date(item_dict["name"],item_dict["start_date"]))

@app.get("/appointment/list/{name}/{start_date}")
async def list_appointment(name,start_date):
    return createResponse(ServiceManager.list_appointment_by_date(name,start_date))

@app.get("/appointment/list-month/{name}/{start_month}")
async def list_appointment_by_month(name,start_month):
    return createResponse(ServiceManager.list_appointment_by_month(name,start_month))

@app.get("/appointment/delete/{name}/{start_date}")
async def delete_appointment_by_date(name,start_date):
    print("Delete appointment by date")
    ServiceManager.delete_appointment_by_date(name,start_date)
    return createResponse(ServiceManager.list_appointment_by_date(name,start_date))

@app.get("/appointment/delete/{name}/{start_date}/{start_time}")
async def delete_appointment_by_datetime(name,start_date,start_time):
    print("Delete appointment by date")
    ServiceManager.delete_appointment_by_datetime(name,start_date,start_time)
    return createResponse(ServiceManager.list_appointment_by_date(name,start_date))
