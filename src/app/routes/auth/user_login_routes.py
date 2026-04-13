from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from jose import jwt, JWTError
from app.services import otp_service
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserInputSchema, SendOtpRequest, VerifyOtpRequest
from app.config import settings
from app.common.db_config import get_db
from app.services import user_service, device_service, otp_service, admin_service
from app.services.unit_of_work import UnitOfWork
from app.common.auth import create_access_token

auth_login_routes = APIRouter(prefix="/api", tags=["auth routes"])


@auth_login_routes.post(
    "/send-otp",
    summary="otp post call by mobile number",
    description="this endpoint is for generate otp for  user through a OTP",
)
async def send_otp(req_body: SendOtpRequest, session: AsyncSession = Depends(get_db)):

    generated_otp = await otp_service.generate_otp()
    response = await otp_service.send_otp(generated_otp)
    req_body.otp = generated_otp

    response = await otp_service.save_otp_in_db(
        req_body, unit_of_work=UnitOfWork(session=session)
    )

    response = {
        "expires_in_minutes": 5,
        "generated_otp": generated_otp,
        "messages": "OTP sent successfully",
    }
    return response


@auth_login_routes.post(
    "/verify-otp",
    summary="otp verification by mobile number",
    description="this endpoint is for verify user through a OTP",
)
async def verify_otp(
    req_body: VerifyOtpRequest, session: AsyncSession = Depends(get_db)
):

    response = await otp_service.verify_otp_service(
        req_body, unit_of_work=UnitOfWork(session=session)
    )
    return response


@auth_login_routes.post(
    "/resend-otp",
    summary="otp post call by mobile number",
    description="this endpoint is for generate otp for  user through a OTP",
)
async def resend_otp(req_body: SendOtpRequest, session: AsyncSession = Depends(get_db)):

    generated_otp = await otp_service.generate_otp()
    response = await otp_service.send_otp(generated_otp)
    req_body.otp = generated_otp

    response = await otp_service.save_otp_in_db(
        req_body, unit_of_work=UnitOfWork(session=session)
    )

    response = {
        "expires_in_minutes": 5,
        "messages": "OTP sent successfully",
    }
    return response


# @auth_login_routes.post(
#     "/users/profile/",
#     summary="registration for new user",
#     description="registration for new user",
# )
# async def new_user(
#     request_body: UserInputSchema, session: AsyncSession = Depends(get_db)
# ):
#     response = await user_service.register_user(
#         request_body, unit_of_work=UnitOfWork(session=session)
#     )
#     return response


# @auth_login_routes.get(
#     "/users/profile/",
#     summary="registration for new user",
#     description="registration for new user",
# )
# async def get_users(session: AsyncSession = Depends(get_db)):
#     response=await user_service.fetch_user(unit_of_work=UnitOfWork(session=session))
#     return response


# @auth_login_routes.post("/refresh")
# def refresh_token(refresh_token: str):

#     payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

#     if payload["type"] != "refresh":
#         raise HTTPException(status_code=401, detail="Invalid token type")

#     token_id = payload["jti"]

#     # check DB
#     token_data = get_refresh_token(token_id)

#     if not token_data or token_data.is_revoked:
#         raise HTTPException(status_code=401, detail="Token revoked")

#     # issue new access token
#     new_access_token = create_access_token(payload["sub"])

#     return {
#         "access_token": new_access_token,
#         "token_type": "bearer"
#     }


@auth_login_routes.post("/logout")
async def logout(refresh_token: str, session: AsyncSession = Depends(get_db)):

    payload = jwt.decode(
        refresh_token, settings.SECRET_KEY_JWT, algorithms=[settings.ALGORITHM]
    )
    token_id = payload["jti"]
    print(token_id)

    await otp_service.revoke_refresh_token(
        token_id, unit_of_work=UnitOfWork(session=session)
    )

    return {"message": "Logged out successfully"}


@auth_login_routes.post("/refresh")
async def refresh_access_token(
    refresh_token: str, session: AsyncSession = Depends(get_db)
):

    response = await otp_service.refresh_access_token(
        refresh_token, unit_of_work=UnitOfWork(session=session)
    )

    return response


@auth_login_routes.post("/auth/super_admin/login")
async def auth_login(
    username: str, password: str, session: AsyncSession = Depends(get_db)
):

    res = await admin_service.super_admin_login_check(
        username=username, password=password, unit_of_work=UnitOfWork(session=session)
    )
    return res


@auth_login_routes.post("/auth/admin/login")
async def auth_login(
    username: str, password: str, session: AsyncSession = Depends(get_db)
):
    print(username, password, 1719777979137917979179)

    res = await admin_service.admin_login_check(
        username=username, password=password, unit_of_work=UnitOfWork(session=session)
    )
    return res
