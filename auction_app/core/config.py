import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('DB_USER')
POSTGRES_PASSWORD = os.getenv('DB_PASSWORD')
POSTGRES_ADDRESS = os.getenv('DB_ADDRESS')
POSTGRES_NAME = os.getenv('DB_NAME')


TEST_POSTGRES_NAME = os.getenv('TEST_DB_NAME', 'test3_db')


DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}/{POSTGRES_NAME}"
)


TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@auction_postgres/{TEST_POSTGRES_NAME}"
)

