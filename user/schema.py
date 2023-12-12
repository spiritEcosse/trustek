from typing import Optional

from ninja import ModelSchema, Schema
from pydantic import EmailStr

from user.models import User

user_fields = ['id', 'email', 'first_name', 'last_name', 'role']


class UserSchema(ModelSchema):
    email: EmailStr

    class Meta:
        model = User
        fields = user_fields


class UserUpdateSchema(ModelSchema):
    email: Optional[EmailStr] = None

    class Meta:
        model = User
        fields = user_fields
        fields_optional = '__all__'


class UserAuthSchema(Schema):
    email: EmailStr
    password: str
