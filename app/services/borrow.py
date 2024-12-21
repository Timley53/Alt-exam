from fastapi import FastAPI, Body, HTTPException
from typing import Annotated, Optional
from uuid import UUID, uuid4
from models import Book, CreateBook, BookUpdate, BorrowBook, BorrowRecord,ReturnBookData
from db import booksDb, borrow_record, usersDb
from datetime import date



class BorrowOperation():

    @staticmethod
    def get_borrow_record_method():
        all_borrow_record = []

        for key, value in borrow_record.items():
            all_borrow_record.append(value)

        return all_borrow_record
    
    @staticmethod
    def borrow_book_method(book_id: UUID, user_id: UUID):
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

        booksDb[book_id]['is_available'] = False
        return {
        'message': 'Book book borrowed successfully'
        }
    

    @staticmethod
    def return_book_method(borrow_record_id:UUID, book_id: UUID, user_id:UUID, ReturnData: Annotated[ReturnBookData, Body(...)]):
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
    
    @staticmethod
    def get_user_borrow_records_method(user_id: UUID):
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



         













