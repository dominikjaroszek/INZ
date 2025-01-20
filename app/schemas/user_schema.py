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
        cls.validate_password(v)
        return v

    @staticmethod
    def validate_password(password: str):
        """Metoda pomocnicza do walidacji haseł."""
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[.!@#$%^&*(),?":{}|<>]', password):
            raise ValueError('Password must contain at least one special character (e.g., ., !, @, etc.)')

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    oldPassword: str
    newPassword : str

    @field_validator('oldPassword', 'newPassword')
    def passwords_must_meet_criteria(cls, v):
        UserRegistrationModel.validate_password(v)
        return v
