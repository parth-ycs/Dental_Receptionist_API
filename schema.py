from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date as Date, datetime




class CreatePatientRequest(BaseModel):
    first_name: str
    last_name: str
    phone: str
    dob: Optional[Date] = None
    email: Optional[str] = None




class BookAppointmentRequest(BaseModel):
    patient_id: str
    doctor_id: str
    start_time: datetime
    reason: Optional[str] = None

    @field_validator("start_time")
    @classmethod
    def require_timezone(cls, value: datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("start_time must include a timezone")
        return value


class CancelAppointmentRequest(BaseModel):
    appointment_id: str


class RescheduleAppointmentRequest(BaseModel):
    appointment_id: str
    new_start_time: datetime

    @field_validator("new_start_time")
    @classmethod
    def require_timezone(cls, value: datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("new_start_time must include a timezone")
        return value
