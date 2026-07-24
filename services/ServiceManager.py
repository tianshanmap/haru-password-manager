from services import PasswordServiceByDB
from services import PasswordServiceByFile
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

