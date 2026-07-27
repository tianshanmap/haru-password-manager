import json
from models.service import *
from utils.files import *
from db.AppointmentManager import singleton_appointment

def create_appointment(item) -> str:
    singleton_appointment.add_appointment(item["name"],item["start_date"],item["start_time"],item["end_time"],item["event"])
    return f"Hello, {item["start_date"]}!"
def delete_appointment_date(name,date: str):
    singleton_appointment.delete_appointment_by_date(name,date)
def delete_appointment_datetime(name,date: str,time):
    singleton_appointment.delete_appointment_by_datetime(name,date,time)
def list_appointments(name,start_date):
    return singleton_appointment.retrieve_appointment_by_date(name,start_date)
def list_appointments_by_month(name,start_month):
    return singleton_appointment.retrieve_appointment_by_month(name,start_month)
