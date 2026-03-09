from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache


from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException

from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/all_hotels", summary="Получение всех отелей без фильтров")
@cache(expire=5)
async def get_hotels_without_filters(db: DBDep):
    return await HotelService(db).get_without_filters()


@router.get("", summary="Получение отелей")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Местонахождения отеля"),
    date_from: date = Query(example="2026-02-04"),
    date_to: date = Query(example="2026-02-10"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}", summary="Получение конкретного отеля")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", summary="Добавление нового отеля")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Beach 5 звезд у моря",
                    "location": "Сочи, ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Sun у фонтана",
                    "location": "Дубай, ул. Шейха, 2",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное изменение отеля")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).update_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
async def partially_edit_hotels(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).partially_edit_hotels(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
