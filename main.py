from fastapi import FastAPI
from datetime import date
from schema import  RescheduleAppointmentRequest, CreatePatientRequest, BookAppointmentRequest, CancelAppointmentRequest

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

# 1. Find Patient - GET
@app.get("/tools/find-patient")
def find_patient(phone: str):
    return {
        "status": "success",
        "message": "Patient found successfully",
        "found": True,
        "patient_id": "PAT-1001",
        "first_name": "Rahul",
    }

# 2. Create Patient - POST
@app.post("/tools/create-patient")
def create_patient(request: CreatePatientRequest):
    return {
        "status": "success",
        "message": "Patient created successfully",
        "patient_id": "PAT-1002",
    }

# 3. List Doctors - GET
@app.get("/tools/list-doctors")
def list_doctors(specialty: str | None = None):
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

    if specialty:
        doctors = [
            doctor
            for doctor in doctors
            if doctor["specialty"].lower() == specialty.lower()
        ]

    return {
        "status": "success",
        "message": "Doctors retrieved successfully",
        "doctors": doctors,
    }

# 4. Get Availability - GET
@app.get("/tools/get-availability")
def get_availability(
    date: date,
    doctor_id: str | None = None,
    date_to: date | None = None,
):
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

    if doctor_id:
        availability = [
            item
            for item in availability
            if item["doctor_id"] == doctor_id
        ]

    # Filter slots by requested date range.
    filtered_availability = []

    for item in availability:
        slots = [
            slot
            for slot in item["slots"]
            if date <= date.fromisoformat(slot[:10])
            and (
                date_to is None
                or date.fromisoformat(slot[:10]) <= date_to
            )
        ]

        if slots:
            filtered_availability.append({
                **item,
                "slots": slots[:5],
            })

    return {
        "status": "success",
        "message": "Availability retrieved successfully",
        "availability": filtered_availability,
    }

# 5. Book Appointment - POST
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

# 6. Get Patient Appointments - GET
@app.get("/tools/get-patient-appointments")
def get_patient_appointments(patient_id: str):
    return {
        "status": "success",
        "message": "Appointments retrieved successfully",
        "patient_id": patient_id,
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

# 7. Cancel Appointment - POST
@app.post("/tools/cancel-appointment")
def cancel_appointment(request: CancelAppointmentRequest):
    return {
        "status": "success",
        "message": "Appointment cancelled successfully",
        "appointment_id": request.appointment_id,
        "status_detail": "cancelled",
    }

# 8. Reschedule Appointment - POST
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
