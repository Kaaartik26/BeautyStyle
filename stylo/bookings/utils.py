from datetime import datetime, timedelta
from services.models import WorkingHour, Break
from .models import Appointment


def overlaps(start, end, blocked_ranges):
    for blocked_start, blocked_end in blocked_ranges:
        if start < blocked_end and end > blocked_start:
            return True
    return False


def generate_time_slots(stylist, service, date):
    weekday = date.weekday()

    working_hours = WorkingHour.objects.filter(
        stylist=stylist,
        day_of_week=weekday
    ).first()

    if not working_hours:
        return []
    
    start_dt = datetime.combine(date, working_hours.start_time)
    end_dt = datetime.combine(date, working_hours.end_time)

    service_duration = timedelta(minutes=service.duration)

    appointments = Appointment.objects.filter(
        stylist=stylist,
        date=date,
        status='BOOKED'
    )

    appointment_ranges = [
        (
            datetime.combine(date, a.start_time),
            datetime.combine(date, a.end_time)
        )
        for a in appointments
    ]

    breaks = Break.objects.filter(
        stylist=stylist,
        date=date
    )

    break_ranges = [
        (
            datetime.combine(date, b.start_time),
            datetime.combine(date, b.end_time)
        )
        for b in breaks
    ]

    slots = []
    current_start = start_dt

    while current_start + service_duration <= end_dt:
        current_end = current_start + service_duration

        if not overlaps(
            current_start,
            current_end,
            appointment_ranges + break_ranges
        ):
            slots.append(
                (current_start.time(), current_end.time())
            )

        current_start += service_duration

    return slots
