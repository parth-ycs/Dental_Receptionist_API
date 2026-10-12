from fastapi import FastAPI
from datetime import date
from schema import FindPatientRequest, AvailabilityRequest, RescheduleAppointmentRequest, CreatePatientRequest, ListDoctorsRequest, BookAppointmentRequest,PatientAppointmentsRequest, CancelAppointmentRequest

app = FastAPI(
    title="Dental Receptionist API",
    description="Mock backend APIs for a dental receptionist voice agent",
    version="1.0.0",
)

@app.get("/")
def home():
    return{
        "status":"welcome to Dental reptionalist"
    }

@app.get("/health")
def health():
    return{
        "status":"ok"
    }

# Request Schemas


# Home & Health

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Welcome to Dental Receptionist API",
    }


@app.get("/health")
def health():
    return {
        "status": "success",
        "message": "API is healthy",
    }


# 1. Find Patient

@app.post("/tools/find-patient")
def find_patient(request: FindPatientRequest):
    return {
        "status": "success",
        "message": "Patient found successfully",
        "found": True,
        "patient_id": "PAT-1001",
        "first_name": "Rahul",
    }


# 2. Create Patient

@app.post("/tools/create-patient")
def create_patient(request: CreatePatientRequest):
    return {
        "status": "success",
        "message": "Patient created successfully",
        "patient_id": "PAT-1002",
    }


# 3. List Doctors

@app.post("/tools/list-doctors")
def list_doctors(request: ListDoctorsRequest):
    doctors = [
        {
            "doctor_id": "DOC-101",
            "name": "Dr. Amit Sharma",
            "specialty": "General Dentistry",
        },
        {
            "doctor_id": "DOC-102",
            "name": "Dr. Priya Mehta",
            "specialty": "Orthodontics",
        },
        {
            "doctor_id": "DOC-103",
            "name": "Dr. Neha Patel",
            "specialty": "Endodontics",
        },
    ]

    if request.specialty:
        doctors = [ doctor for doctor in doctors if doctor["specialty"].lower()== request.specialty.lower()]

    return {
        "status": "success",
        "message": "Doctors retrieved successfully",
        "doctors": doctors,
    }


# 4. Get Availability

@app.post("/tools/get-availability")
def get_availability(request: AvailabilityRequest):
    availability = [
        {
            "doctor_id": "DOC-101",
            "doctor_name": "Dr. Amit Sharma",
            "slots": [
                "2026-10-13T09:00:00+05:30",
                "2026-10-13T10:30:00+05:30",
                "2026-10-13T14:00:00+05:30",
            ],
        },
        {
            "doctor_id": "DOC-102",
            "doctor_name": "Dr. Priya Mehta",
            "slots": [
                "2026-10-13T11:00:00+05:30",
                "2026-10-13T15:00:00+05:30",
            ],
        },
    ]

    if request.doctor_id:
        availability = [ item for item in availability if item["doctor_id"] == request.doctor_id]

    # Return only mock slots matching the requested date.
    availability = [
        {
            **item,
            "slots": [
                slot for slot in item["slots"]
                if date.fromisoformat(slot[:10]) >= request.date
                and (
                    request.date_to is None
                    or date.fromisoformat(slot[:10]) <= request.date_to
                )
            ],
        }
        for item in availability
    ]

    availability = [
        item for item in availability if item["slots"]
    ]

    return {
        "status": "success",
        "message": "Availability retrieved successfully",
        "availability": availability,
    }


# 5. Book Appointment

@app.post("/tools/book-appointment")
def book_appointment(request: BookAppointmentRequest):
    return {
        "status": "success",
        "message": "Appointment booked successfully",
        "appointment_id": "APT-5001",
        "patient_id": request.patient_id,
        "doctor_id": request.doctor_id,
        "doctor_name": "Dr. Amit Sharma",
        "start_time": request.start_time.isoformat(),
        "status": "confirmed",
    }


# 6. Get Patient Appointments

@app.post("/tools/get-patient-appointments")
def get_patient_appointments(
    request: PatientAppointmentsRequest,
):
    return {
        "status": "success",
        "message": "Appointments retrieved successfully",
        "patient_id": request.patient_id,
        "appointments": [
            {
                "appointment_id": "APT-5001",
                "doctor_id": "DOC-101",
                "doctor_name": "Dr. Amit Sharma",
                "start_time": "2026-10-13T09:00:00+05:30",
                "reason": "Dental checkup",
                "status": "confirmed",
            }
        ],
    }


# 7. Cancel Appointment

@app.post("/tools/cancel-appointment")
def cancel_appointment(
    request: CancelAppointmentRequest,
):
    return {
        "status": "success",
        "message": "Appointment cancelled successfully",
        "appointment_id": request.appointment_id,
        "status_detail": "cancelled",
    }


# 8. Reschedule Appointment

@app.post("/tools/reschedule-appointment")
def reschedule_appointment(
    request: RescheduleAppointmentRequest,
):
    return {
        "status": "success",
        "message": "Appointment rescheduled successfully",
        "appointment_id": request.appointment_id,
        "new_start_time": request.new_start_time.isoformat(),
        "status": "rescheduled",
    }
