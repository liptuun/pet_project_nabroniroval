from fastapi import APIRouter
from fastapi_cache.decorator import cache


from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService
from src.tasks.tasks import test_task  # noqa: F401


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение удобств")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_all_facilities()


@router.post("", summary="Добавление удобства")
async def create_facility(db: DBDep, facility_data: FacilityAdd):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}


@router.delete("", summary="Удаление удобства")
async def delete_facility(db: DBDep, facility_id: int):
    await FacilityService(db).delete_facility(facility_id)
    return {"status": "OK"}
