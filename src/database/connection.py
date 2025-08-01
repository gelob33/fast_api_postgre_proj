import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from src.utils.logger import logger
from src.common.exceptions import DatabaseConnectionError

load_dotenv()

DB_URL = os.getenv("postgres_async_url")

def get_engine():
    return create_async_engine(DB_URL, echo=True)

@asynccontextmanager
async def get_conn():
    conn = None
    try:
        conn = await get_engine().connect()
        logger.info("DB connection opened")
        yield conn
    except SQLAlchemyError as e:
        logger.exception(f"DB connection failed!")
        raise DatabaseConnectionError("Database connection failed") from e
    finally:
        if conn is not None:
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

