from src.schema.response import Book
from src.schema.request import CreateBook
from src.common.exceptions import BookNotFoundError, DuplicateBookError
from src.repository.book_repository import book_repo
from typing import List
from uuid import UUID
import uuid


async def get_all_books() -> List[Book]:
    return await book_repo.get_all()


async def get_book_by_id(book_id: UUID) -> Book:
    book = await book_repo.get_by_id(book_id)
    
    if not book:
        raise BookNotFoundError(book_id=book_id)
    
    return book

async def find_books_by_title(book_title: str, fuzzy_search: bool) -> List[Book]:
    books = await book_repo.find_by_title(book_title, fuzzy_search)

    if not books:
        raise BookNotFoundError(title=book_title)
    
    return books        


async def create_book(new_book: CreateBook) -> Book:

    book_title = new_book["title"]
    book_author = new_book["author"]

    # check duplicate book
    exists = await book_repo.find_by_title_author(book_title = book_title, book_author = book_author)

    if exists:
        raise DuplicateBookError(title = book_title, author = book_author)
    else:
        book = await book_repo.create(new_book)

    return book
