from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_user_bookings(
    user_id: UserIdDep,
    db: DBDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    room: Room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    booking_to_add = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    booking = await db.bookings.add_booking(booking_to_add, hotel_id=room.hotel_id)
    await db.commit()
    return {"status": "OK", "data": booking}
