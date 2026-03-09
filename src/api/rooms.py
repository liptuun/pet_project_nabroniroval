from datetime import date
from fastapi import APIRouter, Query, Body

from src.api.dependencies import DBDep
from src.exceptions import (
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException,
    RoomNotFoundException,
    HotelNotFoundException,
)

from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/all_rooms", summary="Получение всех номеров без фильтрации")
async def get_all_rooms(db: DBDep):
    return await RoomService(db).get_without_filters()


@router.get("/{hotel_id}/rooms", summary="Получение номеров")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2026-02-04"),
    date_to: date = Query(example="2026-02-10"),
):
    return await RoomService(db).get_filtered_by_time(
        hotel_id,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение конкретного номера")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Отель Beach",
                "value": {
                    "title": "Комната комфорт в отеле Beach",
                    "description": "Номер типа комфорт на 2 персоны",
                    "price": 1500,
                    "quantity": 2,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Отель Sun",
                "value": {
                    "title": "Комната Люкс в отеле Sun",
                    "description": "Номер типа Lux на 4 персоны со всеми удобствами",
                    "price": 2500,
                    "quantity": 4,
                    "facilities_ids": [1, 2, 3],
                },
            },
        },
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение номера")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение номера")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep,
):
    await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}
