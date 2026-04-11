from app.services.unit_of_work import UnitOfWork
from datetime import datetime, timezone
from app.entities.user_device_entity import UserDeviceEntity


async def check_device(req_body, unit_of_work: UnitOfWork):
    print(77777777373773737377373737373773)
    async with unit_of_work as uow:
        device_entry = await unit_of_work.device_repo.get_device(req_body.device_token)

        if device_entry:
            device_entry.last_login = datetime.now(timezone.utc)
            device_entry.latitude = (device_entry.latitude,)
            device_entry.longitude = device_entry.longitude

        else:
            now = datetime.now(timezone.utc)
            device_entry = UserDeviceEntity(
                user_id=req_body.user_id,
                device_token=req_body.device_token,
                latitude=req_body.latitude,
                longitude=req_body.longitude,
                last_login=now,
            )
            res = await unit_of_work.device_repo.create(device_entry)
            print(res, 2626626266266266262662626262)
        await unit_of_work.commit()

        return res


async def create_device(req_body, unit_of_work: UnitOfWork):
    pass


# implementation


async def get_device(device_id, unit_of_work: UnitOfWork):
    pass
