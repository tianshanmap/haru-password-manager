from pydantic import BaseModel

# 1. Define the data structure using a Pydantic model
class PasswordItem(BaseModel):
    key: str
    username: str
    password: str
    description: str | None = None
class AppointmentItem(BaseModel):
    name: str
    start_date: str
    start_time: str
    end_time: str
    event: str | None = None
    info: str | None = None
    phone: str | None = None
