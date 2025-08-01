import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

DB_URL = os.getenv("postgres_async_url")

def get_engine():
    return create_async_engine(DB_URL, echo=True)

# create async context manager -- @asynccontextmanager 
@asynccontextmanager
async def get_conn():
    conn = await get_engine().connect()
    logger.info("DB connection opened")

    try:
        yield conn
    finally:
        await conn.close()
        logger.info("DB connection closed")


# testing connection
if __name__ == "__main__":
    import asyncio
    async def test_connection():
        async with get_conn() as conn:
            result = await conn.execute(text("SELECT NOW()"))
            current_time = result.scalar()
            print(f"✅ Connected! Current time: {current_time}")

    asyncio.run(test_connection())

