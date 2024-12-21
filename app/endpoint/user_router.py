from fastapi import APIRouter
from crud.user import UserCrud
from fastapi import  Body
from typing import Annotated
from models import CreateUser, User, UpdateUser
from uuid import UUID, uuid4
from models import Book, CreateBook, BookUpdate, BorrowBook, BorrowRecord,ReturnBookData

userRouter = APIRouter()

@userRouter.post("/users", status_code=201) 
async def create_user(user: Annotated[CreateUser, Body(...)],new_user_id: UUID=uuid4()):
    return UserCrud.create_user_method(user)

@userRouter.get('/users', status_code=200)
async def get_all_users():
    return UserCrud.get_all_users_method()

@userRouter.get('/users/{user_id}', status_code=200)
async def get_a_user(userId: UUID):
    return UserCrud.get_a_user_method(userId)

@userRouter.patch('/users/{user_id}', status_code=200)
async def update_user(userId: UUID, updateUser: Annotated[UpdateUser, Body(...)]):
    return UserCrud.update_user_method(userId, updateUser)

@userRouter.delete('/users/{user_id}')
async def delete_user(userId: UUID ):
    return UserCrud.delete_user_method(userId)

@userRouter.put('/users/{user_id}', status_code=200)
async def deactiveate_user(userId: UUID):
    return UserCrud.deactiveate_user_method(userId)

