from typing import Annotated, Optional
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from datetime import date,datetime
from uuid import uuid4
from db import usersDb , booksDb , borrow_record
from models import CreateUser, CreateBook, UpdateUser, BookUpdate, BookAvailable,Book,BorrowBook,BorrowRecord,ReturnBookData,User


app = FastAPI()









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

# deactivate user
@app.put('/users/{user_id}', status_code=200)
def deactiveate_user(userId: UUID):
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


# delete books
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


# make book available
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


# ===========get borrow records=======
@app.get('/books/borrow_record')
def get_borrow_record():
    all_borrow_record = []

    for key, value in borrow_record.items():
        all_borrow_record.append(value)

    return all_borrow_record



# ===========borrow book=======
@app.put('/books/borrow_book/{user_id}', status_code=201)
def borrow_book(book_id: UUID, user_id: UUID):
    book_id = str(book_id)
    user_id = str(user_id)

# if book or user does not exist
    if book_id not in booksDb or user_id not in usersDb:
        raise HTTPException(
            status_code= 404,
            detail='Not found: User or Book not found'
        )
    # if user is not active
    if usersDb[user_id]['is_active'] == False:
         raise HTTPException(
            status_code= 401,
            detail='Unavailable: user not authorized for operation'
        )
    # if book is not available
    if booksDb[book_id]['is_available'] == False:
         raise HTTPException(
            status_code= 401,
            detail='Unavailable: book already borrowed'
        )
    

    new_record_id = uuid4()

    new_record = BorrowRecord(
        id=new_record_id,
        book_id=book_id,
        user_id=user_id,
        borrow_date=date.today(),
        return_date= None
    )

    borrow_record.update({str(new_record_id) : new_record.model_dump()})
    print(borrow_record)

    booksDb[book_id]['is_available'] = False
    return {
       'message': 'Book book borrowed successfully'
    }


# @app.put("/books/borrow_book/{user_id}", status_code=201)
# def borrow_book(book_id: UUID, user_id: UUID):
#     book_id = str(book_id)
#     user_id = str(user_id)

#     if book_id not in booksDb:
#         raise HTTPException(status_code=404, detail="Not found: Book not found")
#     if user_id not in usersDb:
#         raise HTTPException(status_code=404, detail="Not found: User not found")
#     if usersDb[user_id]["is_active"] == False:
#         raise HTTPException(
#             status_code=401, detail="Unavailable: user not authorized for operation"
#         )
#     record_id = str(uuid4())
#     borrow_record[record_id] = {
#         "id": record_id,
#         "book_id": book_id,
#         "user_id": user_id,
#         "borrow_date": date.today(),
#         "return_date": None,
#     }

#     booksDb[book_id]["is_available"] = False
#     return {"message": "Book borrowed successfully"}
#     # borrow_record.update({str(new_record_id) : new_record}) 

# ==============return book==============
@app.put('/books/return_book/{borrow_record_id}')
def return_book(borrow_record_id:UUID, book_id: UUID, user_id:UUID, ReturnData: Annotated[ReturnBookData, Body(...)]):
    borrow_record_id = str(borrow_record_id)
    book_id = str(book_id)
    user_id = str(user_id)
    

# if borrow_record for book does not exist
    if borrow_record_id not in borrow_record:
            raise HTTPException(
                status_code= 404,
                detail='Not found: Book not in borrow record'
            )   
    
    if book_id not in booksDb:
        raise HTTPException(
            status_code= 404,
            detail='Not found: Book does not exist'
        ) 
    if user_id not in usersDb:
        raise HTTPException(
            status_code= 404,
            detail='Not found: User does not exist'
        ) 
    # ===

    # if user is not active
    if usersDb[user_id]['is_active'] == False:
         raise HTTPException(
            status_code= 401,
            detail='Unavailable: user not authorized for operation'
        )
    

    if ReturnData.return_date is not None:
        borrow_record[str(borrow_record_id)]["return_date"] =  ReturnData.return_date
    else:
         borrow_record[str(borrow_record_id)]["return_date"] = date.today()


        # example

    booksDb[book_id]['is_available'] = True

    return {
        'message': 'Book returned succesfully'
    }

# test the return books 




@app.get('/books/borrow_records/{user_id}')
def get_user_borrow_records(user_id: UUID):
    user_id = str(user_id)
    user_borrow_record: list[BorrowRecord] = []



    if user_id not in usersDb:
          raise HTTPException(
            status_code= 404,
            detail='Not found: User does not exist'
        ) 

    for key, record in borrow_record.items():
            if record['user_id'] == user_id:
             user_borrow_record.append(record)

    return user_borrow_record



         

        


