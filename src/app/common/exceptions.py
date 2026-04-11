from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(status_code=status_code, detail=detail)


class BadRequestException(AppException):
    def __init__(self, detail="Bad request"):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)


class ConflictException(AppException):
    def __init__(self, detail="Conflict"):
        super().__init__(detail, status.HTTP_409_CONFLICT)


class NotFoundException(AppException):
    def __init__(self, detail="Not found"):
        super().__init__(detail, status.HTTP_404_NOT_FOUND)


class ForbiddenException(AppException):
    def __init__(self, detail="Forbidden"):
        super().__init__(detail, status.HTTP_403_FORBIDDEN)