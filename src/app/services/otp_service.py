import random
from app.entities.otp_entity import OtpEntity
from app.services.unit_of_work import UnitOfWork
import datetime
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from app.services import user_service, device_service
from app.common import auth
import uuid
from app.config import settings
from jose import jwt, JWTError
from app.common import auth

from app.entities.refresh_token_entity import RefreshTokenEntity


async def send_otp(request):
    # TODO send sms to user mobile number by using third party
    pass


async def generate_otp():
    otp = str(random.randint(100000, 999999))
    return otp


async def save_otp_in_db(req_body, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        now = datetime.now(timezone.utc)
        expire_limit = timedelta(minutes=2)

        entity_obj = OtpEntity(
            mobile_number=req_body.mobile_number,
            otp=req_body.otp,
            is_used=False,
            attempted_count=1,
            expire_at=now + expire_limit,
        )
        result_obj = await unit_of_work.otp_repo.save_otp(entity_obj)

        # raise HTTPException(detail=f"Error occured :{e}, please retry",status_code=status.HTTP_400_BAD_REQUEST)
        return {"message": "otp saved successfully"}


async def verify_otp_service(req_body, unit_of_work: UnitOfWork):
    async with unit_of_work:
        otp_entry = await unit_of_work.otp_repo.get_one(
            req_body.mobile_number, req_body.otp_code
        )
        otp_entry = await unit_of_work.otp_repo.get_one(
            req_body.mobile_number, req_body.otp_code
        )

        _validate_exist(otp_entry)
        _validate_expiry(otp_entry)
        _validate_used(otp_entry)
        _validate_attempts(otp_entry)
        # _validate_match(otp_entry)
        if otp_entry.otp != req_body.otp_code:
            otp_entry.attempted_count += 1
            await unit_of_work.commit()
            raise HTTPException(
                detail="Invalid OTP", status_code=status.HTTP_400_BAD_REQUEST
            )
        otp_entry.is_used = True

        user, is_exist = await user_service.create_user(
            req_body, unit_of_work=unit_of_work
        )
        user_id = user.id
        # req_body.user_id = user_id
        # profile_update = not all([user.name, user.email, user.gender])
        # device_obj = await device_service.check_device(
        #     req_body=req_body, unit_of_work=unit_of_work
        # )
        access_token = auth.create_access_token(
            data={
                "sub": str(user_id),
                "phone": req_body.mobile_number,
                "role": req_body.role,
            }
        )
        # refresh_token, token_id, expire = auth.create_refresh_token(str(user_id))
        # refresh_token, token_id, expire = auth.create_refresh_token(str(user_id))
        # await unit_of_work.refresh_token.save_refresh_token(user_id, token_id, expire)
        # await save_refresh_token(
        #     user_id, token_id, device_obj.id, expire, unit_of_work=unit_of_work
        # )
        # await save_refresh_token(
        #     user_id, token_id, device_obj.id, expire, unit_of_work=unit_of_work
        # )

        return {
            "access_token": access_token,
            # "refresh_token": refresh_token,
            "token_type": "bearer",
            "login_type": "otp",
            "is_exist": is_exist,
            # "profile_update": profile_update,
            "expires_in": 900,
            # "user_id": user_id,
        }

    # return {"message": "OTP validation successful"}


def _validate_exist(otp_entry):
    if not otp_entry:
        raise HTTPException(
            detail="otp requested not found, generate new one",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def _validate_expiry(otp_entry):
    current_time = datetime.now(timezone.utc)
    if otp_entry.expire_at <= current_time:
        raise HTTPException(
            detail="otp got expired, generate new one",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def _validate_used(otp_entry):
    if otp_entry.is_used != False:
        raise HTTPException(
            detail="Otp is already used, generate new one",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # save to repo


def _validate_attempts(otp_entry):
    if otp_entry.attempted_count >= 5:
        raise HTTPException(
            detail="Too many attempts. Please generate new OTP",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # save to repo


async def fetch_otp_entry_from_db(mobile_number, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        result = await unit_of_work.otp_repo.get_one(mobile_number)
        return result


async def update_into_db(obj_in, otp_entry, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        result = await unit_of_work.otp_repo.update(otp_entry, obj_in)
        return result


async def save_refresh_token(
    user_id, token_id, expire, unit_of_work: UnitOfWork, device_id=None
):

    now = datetime.now(timezone.utc)

    entity_obj = RefreshTokenEntity(
        user_id=user_id,
        expires_at=expire,
        token_jti=token_id,
        created_at=now,
        device_id=device_id,
    )
    async with unit_of_work as uow:
        result = await unit_of_work.refresh_token.save_refresh_token(entity_obj)
        return result


async def revoke_refresh_token(token_id, unit_of_work: UnitOfWork):
    async with unit_of_work:
        await unit_of_work.refresh_token.revoke_token(token_jti=token_id)
        await unit_of_work.commit()
        return {"message": "Logged out successfully"}


async def refresh_access_token(refresh_token: str, unit_of_work: UnitOfWork):
    async with unit_of_work:
        # await unit_of_work.refresh_token.revoke_token(token_jti=refresh_token)
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY_JWT, algorithms=[settings.ALGORITHM]
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        # ✅ Validate token type
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")
        token_jti = payload.get("jti")

        if not user_id or not token_jti:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        # ✅ Check DB
        token_data = await unit_of_work.refresh_token.get_one(token_jti)

        if not token_data:
            raise HTTPException(status_code=401, detail="Token not found")

        if token_data.is_revoked:
            raise HTTPException(status_code=401, detail="Token revoked")

        if token_data.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")

        # 🔥 Create new access token

        new_access_token = auth.create_access_token(data={"sub": str(user_id)})
        # Create new refresh token
        new_refresh_token, new_jti, new_expiry = auth.create_refresh_token(user_id)

        await save_refresh_token(
            user_id=user_id,
            token_id=new_jti,
            device_id=token_data.device_id,
            expire=new_expiry,
            unit_of_work=unit_of_work,
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
