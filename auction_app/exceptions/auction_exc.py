from fastapi import Request
from fastapi.responses import JSONResponse


class AuctionException(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code


def auction_exception_handler(request: Request, exc: AuctionException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "detail": exc.detail},
    )