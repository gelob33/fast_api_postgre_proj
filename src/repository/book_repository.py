from sqlalchemy import select, func, insert
from src.database.connection import get_conn
from src.database.schema import BookTable
from src.schema.response import Book
from src.schema.request import CreateBook
from typing import List, Optional
from uuid import UUID
import uuid

# Helper function to avoid repeated code in mappiing resultset to book instsances
def map_row_to_book(row) -> Optional[Book]:
    if row:
        return Book(**dict(row._mapping))
    return None


class BookRepository:
    async def get_all(self) -> List[Book]:
        async with get_conn() as conn:
            stmt = select(BookTable)
            result = await conn.execute(stmt)
            return [map_row_to_book(row) for row in result.fetchall()]

    async def get_by_id(self, book_id: UUID) -> Optional[Book]:
        async with get_conn() as conn:
            stmt = select(BookTable).where(BookTable.c.id == book_id)
            row = (await conn.execute(stmt)).fetchone()
            return map_row_to_book(row)

    async def find_by_title(self, book_title: str, fuzzy: bool) -> List[Book]:
        async with get_conn() as conn:
            if fuzzy:
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

            else:
                stmt = select(BookTable).where(func.lower(BookTable.c.title) == func.lower(book_title))

            result = await conn.execute(stmt, {"title": book_title})
            return [map_row_to_book(row) for row in result.fetchall()]

    async def create(self, book_data: CreateBook) -> Book:
    
        async with get_conn() as conn:
            trans = await conn.begin() # Transaction
            insert_data = dict(book_data)
            insert_data["id"] = uuid.uuid4()
                
            stmt = insert(BookTable).values(**insert_data).returning(BookTable)
            row = (await conn.execute(stmt)).fetchone()
            await trans.commit()      
            return map_row_to_book(row)

# instantiate 
book_repo = BookRepository()