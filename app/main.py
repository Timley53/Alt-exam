from typing import Annotated, Optional
from fastapi import FastAPI
from endpoint.user_router import userRouter
from endpoint.book_router import bookRouter
from endpoint.borrow_router import borrowRouter


app = FastAPI()


app.include_router(userRouter, tags=["users"], prefix="/users")
app.include_router(bookRouter, tags=["books"], prefix="/books")
app.include_router(borrowRouter, tags=["borrow"], prefix="/borrow")
