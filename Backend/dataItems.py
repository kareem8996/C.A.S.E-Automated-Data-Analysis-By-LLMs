"""
This file contains the data items used in the application.
"""
from pydantic import BaseModel,  Field
from typing import Optional,List


class LoginRequest(BaseModel):
    username: str
    password: str

class SignUpRequest(BaseModel):
    first_name:str
    last_name:str
    email:str
    username: str
    password: str


class CreateProject(BaseModel):
    name:str
    user_id: str
    
