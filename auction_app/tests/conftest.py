import asyncio
import pytest
from decimal import Decimal
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from ..main import app
from ..database import get_db, UnitOfWork
from ..core import TEST_DATABASE_URL, LotStatus
from ..models import Base
from ..models import User, Lot
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, poolclass=NullPool)
AsyncSessionTesting = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionTesting() as session:
        yield session
        await session.rollback()


@pytest.fixture(autouse=True)
async def override_get_db(db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app, client=("127.0.0.1", 8000))
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1") as ac:
        yield ac


@pytest.fixture
async def uow(db_session: AsyncSession):
    return UnitOfWork(db_session)


@pytest.fixture
async def create_user(db_session: AsyncSession):
    async def _create(name: str = "Test User"):
        user = User(name=name)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    return _create


@pytest.fixture
async def create_lot(db_session: AsyncSession):
    async def _create(title: str = "Test Lot", price: str = "100.00"):
        end_time_naive = (datetime.now(timezone.utc) + timedelta(hours=1)).replace(tzinfo=None)

        lot = Lot(
            id=uuid4(),
            title=title,
            start_price=Decimal(price),
            current_price=Decimal(price),
            end_time=end_time_naive,
            status=LotStatus.running
        )
        db_session.add(lot)
        await db_session.commit()
        await db_session.refresh(lot)
        return lot

    return _create