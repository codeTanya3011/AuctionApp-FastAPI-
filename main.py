from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auction_app.api.auction_route import auction_router
from auction_app.exceptions.auction_exc import AuctionException, auction_exception_handler
from auction_app.database.db import engine
from auction_app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()


app = FastAPI(
    title="Auction Service API",
    version="1.0.0",
    lifespan=lifespan
)

# щоб фронт підключався без помилок
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AuctionException, auction_exception_handler)

app.include_router(auction_router, prefix="/api/v4/lots")


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to the Auction API",
        "docs": "/docs"
    }