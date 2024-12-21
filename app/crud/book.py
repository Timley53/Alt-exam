from fastapi import FastAPI, Body, HTTPException
from typing import Annotated, Optional
from uuid import UUID, uuid4
from models import Book, CreateBook, BookUpdate, BorrowBook, BorrowRecord,ReturnBookData
from db import booksDb, borrow_record, usersDb
from datetime import date



class BookOperation():

    @staticmethod
    def get_Books_method():
        all_books = []

        for key, book in booksDb.items():
            all_books.append({
                'id': key,
                'book': book
            })
        return all_books
    
    @staticmethod
    def create_book_method(new_book_data: Annotated[CreateBook, Body(...)]):
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
    
    @staticmethod
    def update_book_method(book_id: UUID, update_data: Annotated[BookUpdate, Body(...)]):
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
    
    @staticmethod
    def delete_book_method(book_id:UUID):
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


    @staticmethod
    def is_available_method(book_id: UUID):
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
    
   