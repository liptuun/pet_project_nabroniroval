from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_all_facilities(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, data: FacilityAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()
        return facility

    async def delete_facility(self, facility_id: int):
        await self.db.facilities.delete(id=facility_id)
        await self.db.commit()
