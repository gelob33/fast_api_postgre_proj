import os
from sqlalchemy import select, func, text, Text, insert
from src.schema.response import Book
from src.database.connection import get_conn
from src.database.schema import BookTable
from src.utils.result_mapper import map_row_to_model # abstract method to map rows to model (not in use)
from src.utils import logger
from typing import List
from uuid import UUID
import uuid



async def get_all_books() -> List[Book]:
    async with get_conn() as conn:
        try:
            stmt = select(BookTable)
            result = await conn.execute(stmt)
            rows = result.fetchall()
        except Exception as e:
            logger.exception(f"Get All Books Failed: {e}")
            raise # bubble-up the exception to the api layer

        #return [map_row_to_model(row, Book) for row in rows]
        return [Book(**dict(row._mapping)) for row in rows]

async def get_book_by_id(book_id: UUID) -> Book:
    async with get_conn() as conn:
        try:
            stmt = select(BookTable).where(BookTable.columns.id == book_id)
            result = await conn.execute(stmt)
            row = result.fetchone()   
        except Exception as e:
            raise 

        #return map_row_to_model(row, Book)
        return Book(**dict(row._mapping))


async def get_book_by_title(book_title: str, fuzzy_search: bool) -> List[Book]:
    async with get_conn() as conn:
        try:
            if fuzzy_search:
                # to allow for fuzzy search in PostgreSQL ensure ppg_trgm extension enabled

                # using similarity sqlalchemy core
                stmt = (
                    select(BookTable)
                    .where(func.play_pen.similarity(BookTable.c.title, book_title) > 0.3)
                    .order_by(func.play_pen.similarity(BookTable.c.title, book_title).desc())
                )

                # using similarity sql statement
                # stmt = text("""SELECT bk.* 
                #                  FROM play_pen.book bk
                #                 WHERE play_pen.SIMILARITY(bk.title, :title) > 0.3 
                #                 ORDER BY play_pen.SIMILARITY(bk.title, :title) DESC;""")
            
                # using levenshtein's fuzzystrmatch
                # stmt = text("""SELECT bk.* 
                #                  FROM play_pen.book bk
                #                 WHERE play_pen.LEVENSHTEIN(CAST(bk.title AS TEXT), CAST(:title AS TEXT)) < 3
                #                 ORDER BY play_pen.LEVENSHTEIN(CAST(bk.title AS TEXT), CAST(:title AS TEXT)) ASC;""")                

                result = await conn.execute(stmt, {"title": book_title})

            else:
                stmt = select(BookTable).where(func.lower(BookTable.c.title) == func.lower(book_title))
                result = await conn.execute(stmt)     

            rows = result.fetchall()
        
            #return [map_row_to_model(row, Book) for row in rows]
            return [Book(**dict(row._mapping)) for row in rows]            
        except Exception as e:
            raise


async def create_book(book_data: dict) -> Book:

    async with get_conn() as conn:
        trans = await conn.begin()

        try:
            book_data["id"] = str(uuid.uuid4())
            stmt = (insert(BookTable).values(**book_data))
            result = await conn.execute(stmt.returning(BookTable))
            await trans.commit()                        
            row = result.fetchone()
            return Book(**dict(row._mapping))

        except Exception as e:
            await trans.rollback()
            raise
