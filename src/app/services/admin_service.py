from app.services.unit_of_work import UnitOfWork
from app.common import utils
from app.entities.user_entity import UserEntity
from app.entities.driver_entity import DriverEntity
from app.common import auth
from datetime import datetime, timedelta, timezone
from app.services.otp_service import save_refresh_token
from app.common.exceptions import ConflictException


async def create_admin(current_user, request, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:

        # 1. Authorization check
        if current_user.get("role") != "super_admin":
            raise Exception("Only super admin can create admin")

        # 2. Check username already exists
        existing_user = await uow.user_repo.get_by_username(request.username)
        if existing_user:
            raise Exception("Username already exists")

        # 3. Hash password
        hashed_password = utils.hash_password(request.password)
        username = request.username.strip().lower()
        user_entity = UserEntity(
            username=username,
            password_hash=str(hashed_password),
            role="admin",
            name=request.name,
        )

        new_user = await uow.user_repo.add_user(user_entity)

        return {
            "message": "Admin created successfully",
            "user_id": str(new_user.id),
            "role": user_entity.role,
        }


async def create_driver(current_user, request, unit_of_work):
    """Create a driver by admin or superadmin"""

    async with unit_of_work as uow:
        # 1. Authorization (super_admin only for now)
        if current_user.get("role") not in ["super_admin", "admin"]:
            raise Exception("Only super admin and  admin allowed")

        mobile_number = request.mobile_number.strip()
        if (
            not mobile_number
            or not request.license_number
            or not request.aadhaar_number
        ):
            raise Exception("Missing required fields")
        existing_user = await uow.user_repo.get_one(mobile_number)

        if existing_user:
            if existing_user.role == "driver":
                raise Exception("Driver already exists with this mobile number")

            # If passenger → convert to driver OR reject
            raise Exception("User already exists with different role")
        # 5. Check duplicate Aadhaar (VERY IMPORTANT)
        existing_driver = await uow.driver_repo.get_by_aadhaar(request.aadhaar_number)
        if existing_driver:
            raise Exception("Driver already exists with this Aadhaar number")

        # 6. Create UserEntity
        user_entity = UserEntity(
            mobile_number=mobile_number,
            role="driver",
            name=request.name,
            gender=request.gender,
            profile_pic=request.profile_pic,
        )

        new_user = await uow.user_repo.add_user(user_entity)
        # 7. Create DriverEntity
        driver_entity = DriverEntity(
            user_id=new_user.id,
            license_number=request.license_number,
            aadhaar_number=request.aadhaar_number,
            name=request.name,
            is_verified=False,
        )

        # Handle optional DOB
        if request.dob:
            driver_entity.dob = request.dob

        await uow.driver_repo.add_driver(driver_entity)

        return {"message": "Driver created successfully", "user_id": str(new_user.id)}


async def admin_login_check(username, password, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        admin = await uow.user_repo.get_by_username(username=username)
        if not admin:
            raise Exception(
                "Incorrect Username !, Please enter correct usernmae and try again "
            )
        

        matched_password = await utils.match_password(
            password=password, stored_pw=admin.password_hash
        )
        if not matched_password:
            raise Exception("Insert correct password")
        data = {"user_id": str(admin.id), "role": admin.role}
        expire = timedelta(days=15)
        result = auth.create_access_token(data=data, expires_delta=expire)
        return {"access_token": result, "role": "admin"}



async def super_admin_login_check(username, password, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        super_admin = await uow.user_repo.get_by_username(username=username)
        
        if not super_admin:
            raise Exception(
                "Incorrect Username !, Please enter correct usernmae and try again "
            )

        matched_password = await utils.match_password(
            password=password, stored_pw=super_admin.password_hash
        )
        if not matched_password:
            raise Exception("Insert correct password")
        data = {"user_id": str(super_admin.id), "role": super_admin.role}
        expire = timedelta(days=15)
        result = auth.create_access_token(data=data, expires_delta=expire)
        return {"access_token": result, "role": "super_admin"}
        # refresh_token, token_id, expire = auth.create_refresh_token(str(user_id))
        # await save_refresh_token(
        #     user_id, token_id, device_obj.id, expire, unit_of_work=unit_of_work
        # )



async def fetch_all_drivers(current_user, unit_of_work):
    async with unit_of_work as uow:
        if current_user.get("role") not in ["super_admin", "admin"]:
            raise ConflictException("Only super admin and  admin allowed")
        
        pass
        

        





