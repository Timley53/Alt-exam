from fastapi import FastAPI, Body, HTTPException
from typing import Annotated, Optional
from uuid import UUID, uuid4
from models import CreateUser, User, UpdateUser
from db import usersDb



class UserCrud():

    # create users
    @staticmethod
    def create_user_method(user: Annotated[CreateUser, Body(...)],new_user_id: UUID=uuid4()):
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
    @staticmethod
    def get_all_users_method():
        all_Users = []
        for id, user in usersDb.items():
            all_Users.append({
            'id': id,
            'user': user
         })

        return all_Users
    
    # get a single user
    @staticmethod
    def get_a_user_method(userId: UUID):
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
    @staticmethod
    def update_user_method(userId: UUID, updateUser: Annotated[UpdateUser, Body(...)]):
        userId = str(userId)
        for key, value in updateUser.model_dump().items():
            if value != None:
                usersDb[userId][key] = value
        
        return {
            'user': usersDb[userId]
        }
    
    # delete user
    @staticmethod
    def delete_user_method(userId: UUID ):
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
    @staticmethod
    def deactiveate_user_method(userId: UUID):
        userId = str(userId)
        for key, value in usersDb.items():
            if key == userId:
                usersDb[userId]['is_active'] = False
        
        return {
            'is_active': usersDb[userId].get('is_active')
        }


    





