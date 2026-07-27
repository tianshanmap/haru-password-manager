from services import PasswordServiceByDB
from services import PasswordServiceByFile
from services import AppointmentServiceByDB
isDB = True
def create_user(item) -> str:
    if isDB:
        return PasswordServiceByDB.create_user(item)
    else:
        return PasswordServiceByFile.create_user(item)
def update_user(item) -> str:
    if isDB:
        return PasswordServiceByDB.update_user(item)
    else:
        return PasswordServiceByFile.update_user(item)
def delete_user(key: str):
    if isDB:
        return PasswordServiceByDB.delete_user(key)
    else:
        return PasswordServiceByFile.delete_user(key)
def list_users():
    if isDB:
        return PasswordServiceByDB.list_users()
    else:
        return PasswordServiceByFile
def backup():
    if isDB:
        return PasswordServiceByDB.backup()
def export_password():
    if isDB:
        return PasswordServiceByDB.export()
def import_password(content):
    if isDB:
        return PasswordServiceByDB.import_password(content)

def create_appointment(item) -> str:
    return AppointmentServiceByDB.create_appointment(item)
def delete_appointment_by_date(name,start_date: str):
    return AppointmentServiceByDB.delete_appointment_date(name,start_date)
def delete_appointment_by_datetime(name,start_date: str,start_time):
    return AppointmentServiceByDB.delete_appointment_datetime(name,start_date,start_time)
def list_appointment_by_date(name,start_date: str):
    list_of_appointment = AppointmentServiceByDB.list_appointments(name,start_date)
    if list_of_appointment == None:
        return []
    return list_of_appointment
def list_appointment_by_month(name,start_month: str):
    list_of_appointment = AppointmentServiceByDB.list_appointments_by_month(name,start_month)
    if list_of_appointment == None:
        return []
    return list_of_appointment