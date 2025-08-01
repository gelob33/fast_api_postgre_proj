from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from src.schema.request import CreateBook
from src.schema.response import Book
from src.services import book_service
from typing import List
from uuid import UUID
from src.utils.logger import logger
from src.common.exceptions import AppError

app = FastAPI()


@app.get("/books", response_model=List[Book])
async def get_all_books():
    return await book_service.get_all_books()


@app.get("/books/", response_model=List[Book])
async def get_book_by_title(book_title: str, fuzzy_search: bool = False):
    books = await book_service.get_book_by_title(book_title, fuzzy_search)

    if not books:
        raise HTTPException(status_code=404, detail=f"Book '{book_title}' not found")
    
    return books


@app.get("/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: UUID):
    books = await book_service.get_book_by_id(book_id)

    if not books:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")
    
    return books


@app.post("/books/create_book", response_model=Book)
async def create_book(new_book: CreateBook = Body(...)):
    book = await book_service.create_book(new_book.model_dump())
    return book


@app.exception_handler(Exception)
async def generic_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    logger.error(f"App error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

