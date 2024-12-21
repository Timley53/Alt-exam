from fastapi import APIRouter
from crud.book import BookOperation
from fastapi import Body
from typing import Annotated
from uuid import UUID
from models import CreateBook, BookUpdate 


bookRouter = APIRouter()

@bookRouter.get('/books', status_code=200)
async def get_Books():
    return BookOperation.get_Books_method()

@bookRouter.post('/books', status_code=201)
async def create_book(new_book_data: Annotated[CreateBook, Body(...)]):
    return BookOperation.create_book_method(new_book_data)

@bookRouter.patch('/books/{book_id}', status_code=200)
async def update_book(book_id: UUID, update_data: Annotated[BookUpdate, Body(...)]):
    return BookOperation.update_book_method(book_id, update_data)

@bookRouter.delete('/books/{book_id}')
async def delete_book(book_id:UUID):
    return BookOperation.delete_book_method(book_id)

@bookRouter.put('/books/{book_id}')
async def is_available(book_id: UUID):
    return BookOperation.is_available_method(book_id)