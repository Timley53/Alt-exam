from typing import Annotated, Optional
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from app.db import usersDb , booksDb

app = FastAPI()



class CreateUser(BaseModel):
    username: str
    full_name: str
    email: EmailStr

class User(CreateUser):
    id: UUID
    is_active: bool = True

class UpdateUser(BaseModel):
    username: str | None = None
    full_name: str | None = None
    email: EmailStr | None = None


# ===========Books Model============= 

class CreateBook(BaseModel):
    title: str
    author: str


class Book(CreateBook):
    id:UUID
    is_available: bool = True
    

class BookUpdate(BaseModel):
     title: str | None = None
     author: str | None = None

class BookAvailable(BaseModel):
    id: UUID 
    is_available: bool = True




# create users
@app.post("/users", status_code=201) 
def create_user(user: Annotated[CreateUser, Body(...)],new_user_id: UUID=uuid4()):
    for key, users in usersDb.items():
        if users.get('email') == user.email or users.get('username') == user.username:
            raise HTTPException(
                status_code=400, 
                detail= 'email or username already registered'
            )
    new_user_id = uuid4()
    new_user = User(
        id=new_user_id,
        **user.model_dump()
        ) 
    usersDb[new_user_id] = new_user.model_dump()  # research
    return {'id': new_user_id,
            'user': usersDb[new_user_id]
            }

# read all users
@app.get('/users', status_code=200)
def get_all_users():
    all_Users = []
    for id, user in usersDb.items():
        all_Users.append({
            'id': id,
            'user': user
        })

    return all_Users

# read a single user

@app.get('/users/{user_id}', status_code=200)
def get_a_user(userId: UUID):
    userId= str(userId)
    if userId not in usersDb:
        raise HTTPException(
            status_code=404,
            detail='Id does not match any user'
        )
    return {
        'id': userId,
        "user": usersDb[userId]
    }

# update a user
@app.patch('/users/{user_id}', status_code=200)
def update_user(userId: UUID, updateUser: Annotated[UpdateUser, Body(...)]):
    userId = str(userId)
    for key, value in updateUser.model_dump().items():
        if value != None:
            usersDb[userId][key] = value
    
    return {
        'user': usersDb[userId]
    }

  
# delete user 
@app.delete('/users/{user_id}')
def delete_user(userId: UUID ):
    userId = str(userId)
    if userId not in usersDb:
        raise HTTPException(
        status_code=404,
        detail='user not found'
    )
    del usersDb[userId]
    
    return {   
     'message': 'User deleted successfully'
 }


@app.put('/users/{user_id}', status_code=200)
def is_active(userId: UUID):
    userId = str(userId)
    for key, value in usersDb.items():
        if key == userId:
            usersDb[userId]['is_active'] = False
    
    return {
        'is_active': usersDb[userId].get('is_active')
    }



# ==============Books endpoint===========


# read books
@app.get('/books', status_code=200)
def get_Books():
    all_books = []

    for key, book in booksDb.items():
        all_books.append({
            'id': key,
            'book': book
        })
    return all_books

@app.post('/books', status_code=201)
def create_book(new_book_data: Annotated[CreateBook, Body(...)]):
    new_book_id : UUID = uuid4() 
    for key, book in booksDb.items():
        if book.get('author') == new_book_data.author and book.get('title') == new_book_data.title:
            raise HTTPException(
                status_code= 409,
                detail='Duplicate Entry: Book already exists'
            )
    
    new_book = Book(
        id=new_book_id,
        **new_book_data.model_dump()
    )
    booksDb[new_book_id] = new_book.model_dump()  

    return {'id': new_book_id,
            'book': booksDb[new_book_id]
            }


@app.patch('/books/{book_id}', status_code=200)
def update_book(book_id: UUID, update_data: Annotated[BookUpdate, Body(...)]):
    book_id = str(book_id)
    if book_id not in booksDb:
        raise HTTPException(
            status_code=404,
            detail='Not Found: No Match'
        )

    booksDb[book_id] = {
        **booksDb[book_id],
        **update_data.model_dump(exclude_unset=True)
    } 
    return {
        'id': book_id,
        'book': booksDb[book_id]
    }

@app.delete('/books/{book_id}')
def delete_book(book_id:UUID):
    book_id = str(book_id)
    if book_id not in booksDb:
        raise HTTPException(
            status_code=404,
            detail='Not Found: No Match'
        )
    del booksDb[book_id]
    return {
        "message": 'Book succefully deleted'
    }



@app.put('/books/{book_id}')
def is_available(book_id: UUID):
    book_id = str(book_id)
    if book_id not in booksDb:
        raise HTTPException(
            status_code=404,
            detail='Not Found: No Match'
        )
    booksDb[book_id]['is_available'] = False
    return {
        'id': book_id,
        'book': booksDb[book_id]
    }


