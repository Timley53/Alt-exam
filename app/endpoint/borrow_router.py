from fastapi import APIRouter
from crud.user import UserCrud
from crud.book import BookOperation
from services.borrow import BorrowOperation
from fastapi import FastAPI, Body, HTTPException
from typing import Annotated, Optional
from models import CreateUser, User, UpdateUser
from uuid import UUID, uuid4
from models import Book, CreateBook, BookUpdate, BorrowBook, BorrowRecord,ReturnBookData


borrowRouter = APIRouter()


@borrowRouter.get('/books/borrow_record')
async def get_borrow_record():
    return BorrowOperation.get_borrow_record_method()

@borrowRouter.put('/books/borrow_book/{user_id}', status_code=201)
async def borrow_book(book_id: UUID, user_id: UUID):
    return BorrowOperation.borrow_book_method(book_id, user_id)

@borrowRouter.put('/books/return_book/{borrow_record_id}')
async def return_book(borrow_record_id:UUID, book_id: UUID, user_id:UUID, ReturnData: Annotated[ReturnBookData, Body(...)]):
    return BorrowOperation.return_book_method(borrow_record_id, book_id, user_id,ReturnData)

@borrowRouter.get('/books/borrow_records/{user_id}')
async def get_user_borrow_records(user_id: UUID):
    return BorrowOperation.get_user_borrow_records_method(user_id)