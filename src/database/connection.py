import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from src.utils.logger import logger
from src.common.exceptions import DatabaseConnectionError
import asyncio
import socket

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
    # capture query, connection pool timeouts (SQLAlchemyError), 
    # database timeouts errors (asyncio),
    # OS level errors, including file I/O, permission issues, and low-level socket failures network related failures 
    # like refused connections, broken pipes, or unreachable hosts(OSerror)
    except SQLAlchemyError as e:
        logger.exception("Invalid SQL syntax")
        raise DatabaseConnectionError("Invalid SQL Syntax!") from e    
    except (OSError, asyncio.TimeoutError) as e:
        logger.exception("Database connection failed")
        raise DatabaseConnectionError("Database connection failed") from e
    except Exception as e:
        logger.exception(f"Unexpected DB error!")  
        raise DatabaseConnectionError("Unexpected database error") from e              
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

