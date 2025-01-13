from pydantic import BaseModel, EmailStr, StringConstraints,Field
from typing_extensions import Annotated
from typing import Optional
from pydantic import field_validator
import re


class UserRegistrationModel(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str

    @field_validator('firstName', 'lastName')
    def names_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('must contain only letters')
        return v

    @field_validator('password')
    def password_must_meet_criteria(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[.!@#$%^&*(),?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character (e.g., ., !, @, etc.)')
        return v
    
class UserUpdateModel(BaseModel):  
    phoneNumber: Optional[str] = Field(None, min_length=9, max_length=9)
    name: Optional[str] = None
    surname: Optional[str] = None

    @field_validator('name', 'surname')
    def names_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('must contain only letters')
        return v

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

class UserSearchModel(BaseModel):
    name: str
    surname: str
    email: EmailStr

    @field_validator('name', 'surname')
    def names_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('must contain only letters')
        return v

class UserUpdate(BaseModel):
    oldPassword: str
    newPassword : str

    @field_validator('oldPassword')
    def password_must_meet_criteria(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[.!@#$%^&*(),?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character (e.g., ., !, @, etc.)')
        return v
    
    @field_validator('newPassword')
    def password_must_meet_criteria(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[.!@#$%^&*(),?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character (e.g., ., !, @, etc.)')
        return v
