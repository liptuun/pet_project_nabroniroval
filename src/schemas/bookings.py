from datetime import date

from pydantic import BaseModel


class BookingAdd(BaseModel):
    date_from: date
    date_to: date
    room_id: int
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int
