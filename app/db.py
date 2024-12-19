from models import BorrowRecord

usersDb = {
    '34e9b31a-85c8-46f3-98d1-f8b7d4e2c0a5': {
        'username': 'úsername 1' ,
        "full_name": 'full name1',
        'email': 'email1@gmail.com' ,
        'is_active': True,
    },
    'e029a4f6-1d93-4b8c-a7f9-3d1c88b5f627': {
        'username': 'úsername 2' ,
        "full_name": 'full name2',
        'email': 'email2@gmail.com' ,
        'is_active': True,
    },
    '9cb1d32e-05a4-4c7b-828a-7f9e31c4a58d': {
        'username': 'úsername 3' ,
        "full_name": 'full name3',
        'email': 'email3@gmail.com' ,
        'is_active': True,
    },
}


booksDb = {
    'b1be97a1-4ecf-4c35-b5ed-d0b9acad1f4f': {
        'id': 'b1be97a1-4ecf-4c35-b5ed-d0b9acad1f4f',
        'title': 'Book 1',
        'author': 'Author 1',
        'is_available': True
    },
    'c4f02419-6c87-43bb-8ae8-90d75d6e3fab': {
        'id': 'c4f02419-6c87-43bb-8ae8-90d75d6e3fab',
        'title': 'Book 2',
        'author': 'Author 2',
        'is_available': True
    },
}


borrow_record = {
    '550e8400-e29b-41d4-a716-446655440000':{
        'id': '550e8400-e29b-41d4-a716-446655440000',
        'book_id': 'b1be97a1-4ecf-4c35-b5ed-d0b9acad1f4f',
        'user_id': '9cb1d32e-05a4-4c7b-828a-7f9e31c4a58d',
        'borrow_date': '2024-11-15',
        'return_date': None
    },

    'ac9d1d43-5c33-4e8c-b3b7-0320220f8984':{
        'id': 'ac9d1d43-5c33-4e8c-b3b7-0320220f8984',
        'book_id': 'c4f02419-6c87-43bb-8ae8-90d75d6e3fab',
        'user_id': '34e9b31a-85c8-46f3-98d1-f8b7d4e2c0a5',
        'borrow_date': '2024-10-15',
        'return_date': '2024-10-25'
    }
}



# print('550e8400-e29b-41d4-a716-446655440000' in borrow_record.keys())



# 550e8400-e29b-41d4-a716-446655440000
# 3e92b7d5-ae2c-4c23-8e55-59e163a02c9a
# 09b1e284-ecc1-4055-b083-bf3671070528
# ac9d1d43-5c33-4e8c-b3b7-0320220f8984
# 7b56cd99-5fe8-4c63-bc92-e4e21891747f



# b1be97a1-4ecf-4c35-b5ed-d0b9acad1f4f  
# c4f02419-6c87-43bb-8ae8-90d75d6e3fab  
# d8cd5d92-d921-4c7f-b7ce-453ba62f7517  
# 09cdf9a0-d4fb-4d1b-8f17-a78d2a9f53e5  
# 0c17ce51-6401-40f0-8e4d-6b7623d72a51