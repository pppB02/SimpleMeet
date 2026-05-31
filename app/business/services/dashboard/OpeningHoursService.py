from datetime import time

from app import db
from ....db_models import OpeningHour

WEEKDAYS = [
    ("mon", 0),
    ("tue", 1),
    ("wed", 2),
    ("thu", 3),
    ("fri", 4),
    ("sat", 5),
    ("sun", 6),
]


def _build_time(hour, minute):
    return time(hour=int(hour), minute=int(minute))


def save_opening_hours(business_id: int, form):
    for prefix, day_of_week in WEEKDAYS:
        open_hour = getattr(form, f"{prefix}OpenHour").data
        open_min = getattr(form, f"{prefix}OpenMin").data
        close_hour = getattr(form, f"{prefix}CloseHour").data
        close_min = getattr(form, f"{prefix}CloseMin").data
        closed = getattr(form, f"{prefix}Closed").data

        row = OpeningHour.query.filter_by(
            business_id=business_id,
            day_of_week=day_of_week,
        ).first()

        if not row:
            row = OpeningHour(
                business_id=business_id,
                day_of_week=day_of_week,
            )

        row.is_closed = bool(closed)

        if closed:
            row.open_time = None
            row.close_time = None
        else:
            row.open_time = _build_time(open_hour, open_min)
            row.close_time = _build_time(close_hour, close_min)

        db.session.add(row)
    print("Saved")
    db.session.commit()


def load_opening_hours_to_form(business_id: int, form):
    rows = OpeningHour.query.filter_by(business_id=business_id).all()
    row_map = {row.day_of_week: row for row in rows}

    for prefix, day_of_week in WEEKDAYS:
        row = row_map.get(day_of_week)
        print(row)
        if not row:
            continue
        
        print(prefix)
        getattr(form, f"{prefix}Closed").data = row.is_closed

        if row.open_time:
            getattr(form, f"{prefix}OpenHour").data = row.open_time.hour
            getattr(form, f"{prefix}OpenMin").data = row.open_time.minute

        if row.close_time:
            getattr(form, f"{prefix}CloseHour").data = row.close_time.hour
            getattr(form, f"{prefix}CloseMin").data = row.close_time.minute