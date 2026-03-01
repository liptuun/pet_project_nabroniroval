from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest

from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all()


@router.get("/me")
async def get_user_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_filtered_bookings(user_id)


@router.post("")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    try:
        booking = await BookingService(db).create_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}
