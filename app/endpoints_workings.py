from fastapi import FastAPI, Body, HTTPException
from typing import Annotated, Optional
from models import CreateUser, User, UpdateUser
from uuid import UUID, uuid4
from crud.user import UserCrud
from crud.book import BookOperation
from services.borrow import BorrowOperation
from models import Book, CreateBook, BookUpdate, BorrowBook, BorrowRecord,ReturnBookData

app = FastAPI()


# user endpoints
@app.post("/users", status_code=201) 
async def create_user(user: Annotated[CreateUser, Body(...)],new_user_id: UUID=uuid4()):
    return UserCrud.create_user_method(user)

@app.get('/users', status_code=200)
async def get_all_users():
    return UserCrud.get_all_users_method()

@app.get('/users/{user_id}', status_code=200)
async def get_a_user(userId: UUID):
    return UserCrud.get_a_user_method(userId)

@app.patch('/users/{user_id}', status_code=200)
async def update_user(userId: UUID, updateUser: Annotated[UpdateUser, Body(...)]):
    return UserCrud.update_user_method(userId, updateUser)

@app.delete('/users/{user_id}')
async def delete_user(userId: UUID ):
    return UserCrud.delete_user_method(userId)

@app.put('/users/{user_id}', status_code=200)
async def deactiveate_user(userId: UUID):
    return UserCrud.deactiveate_user_method(userId)


# book end points
@app.get('/books', status_code=200)
async def get_Books():
    return BookOperation.get_Books_method()

@app.post('/books', status_code=201)
async def create_book(new_book_data: Annotated[CreateBook, Body(...)]):
    return BookOperation.create_book_method(new_book_data)

@app.patch('/books/{book_id}', status_code=200)
async def update_book(book_id: UUID, update_data: Annotated[BookUpdate, Body(...)]):
    return BookOperation.update_book_method(book_id, update_data)

@app.delete('/books/{book_id}')
async def delete_book(book_id:UUID):
    return BookOperation.delete_book_method(book_id)

@app.put('/books/{book_id}')
async def is_available(book_id: UUID):
    return BookOperation.is_available_method(book_id)

# borrow book endpoints

@app.get('/books/borrow_record')
async def get_borrow_record():
    return BorrowOperation.get_borrow_record_method()

@app.put('/books/borrow_book/{user_id}', status_code=201)
async def borrow_book(book_id: UUID, user_id: UUID):
    return BorrowOperation.borrow_book_method(book_id, user_id)

@app.put('/books/return_book/{borrow_record_id}')
async def return_book(borrow_record_id:UUID, book_id: UUID, user_id:UUID, ReturnData: Annotated[ReturnBookData, Body(...)]):
    return BorrowOperation.return_book_method(borrow_record_id, book_id, user_id,ReturnData)

@app.get('/books/borrow_records/{user_id}')
async def get_user_borrow_records(user_id: UUID):
    return BorrowOperation.get_user_borrow_records_method(user_id)