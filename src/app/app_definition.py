from fastapi import FastAPI, Request, HTTPException, status
from app.routes.auth.user_login_routes import auth_login_routes
from app.routes.user_routes import user_routes
from fastapi.exceptions import HTTPException
from app.routes import passenger_routes
from app.routes import driver_routes
from app.routes import super_admin_routes
from app.routes import admin_routes
from app.routes.vehicle_routes import vehicle_route
from app.routes.trip_routes import trip_route
from app.routes.booking_routes import booking_route

from fastapi.responses import JSONResponse

servers = [
    {
        "url": "http://localhost:9000",
        "description": "Local environment",
    }
    # {
    #     "url": "https://devaetelmar-api.annalect.com/",
    #     "description": "Develop environment",
    # },
    # {
    #     "url": "https://qaaetelmar-api.annalect.com/",
    #     "description": "QA environment",
    # },
    # {
    #     "url": "https://stgaetelmar-api.annalect.com/",
    #     "description": "STG environment",
    # },
    # {
    #     "url": "https://aetelmar-api.annalect.com/",
    #     "description": " PROD environment",
    # },
]


travel_agency_api = FastAPI(
    title="TRAVEL AGENCY API",
    summary="Travel agency api",
    version="0.0.1",
    servers=servers,
)


travel_agency_api.include_router(auth_login_routes)
travel_agency_api.include_router(user_routes)

travel_agency_api.include_router(passenger_routes.passenger_route)
travel_agency_api.include_router(driver_routes.driver_route)
travel_agency_api.include_router(super_admin_routes.super_admin_route)
travel_agency_api.include_router(admin_routes.admin_route)
travel_agency_api.include_router(vehicle_route)
travel_agency_api.include_router(trip_route)
travel_agency_api.include_router(booking_route)


# defined exception handlers
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None,
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Something went wrong",
            "data": None,
        },
    )


# register handlers in application
travel_agency_api.add_exception_handler(HTTPException, http_exception_handler)
travel_agency_api.add_exception_handler(Exception, general_exception_handler)
