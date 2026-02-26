from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache


from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, check_date_to_after_date_from, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение списка отелей")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Местонахождения отеля"),
    date_from: date = Query(example="2026-02-04"),
    date_to: date = Query(example="2026-02-10"),
):
    check_date_to_after_date_from(date_to, date_from)
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1),
    )


@router.get("/{hotel_id}", summary="Получение конкретного отеля")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", summary="Добавление нового отеля в список")
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное изменение отеля")
async def update_hotels(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле: можно обновить name, а можно title",
)
async def partially_edit_hotels(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля из списка")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
