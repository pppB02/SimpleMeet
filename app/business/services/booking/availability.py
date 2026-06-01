# app/business/services/booking/availability.py
from datetime import datetime, timedelta


def generate_slots(date, open_time, close_time, duration_minutes, existing_appointments):
    slots = []
    current = datetime.combine(date, open_time)
    day_end = datetime.combine(date, close_time)
    duration = timedelta(minutes=duration_minutes)

    while current + duration <= day_end:
        slot_end = current + duration

        overlap = any(
            current < appointment.end_at and slot_end > appointment.start_at
            for appointment in existing_appointments
        )

        if not overlap:
            slots.append({
                "start_at": current,
                "end_at": slot_end
            })

        current += duration

    return slots