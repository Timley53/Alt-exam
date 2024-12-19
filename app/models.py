from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from datetime import date,datetime


# =====user models
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


# ====borrow book models====
class BorrowBook(BaseModel):
    book_id: UUID
    user_id: UUID


class BorrowRecord(BorrowBook):
    id: UUID
    borrow_date: date
    return_date: date | None = None

class ReturnBookData(BaseModel):
    return_date: date | None = None


