from pydantic import BaseModel
from datetime import datetime, date
from typing import Union

class User(BaseModel):
	username: str
	password: str
	birthday: date
	create_time: datetime
	last_login: datetime

	class Config:
		orm_mode = True


class UserCreate(BaseModel):
	username: str
	password: str
	birthday: date

	class Config:
		orm_mode = True

class UserInDB(BaseModel):
	username: str
	password: str	#hashed_password
	birthday: date
	create_time: datetime
	last_login: datetime

class UserUpdate(BaseModel):
	password: Union[str, None] = None
	birthday: Union[date, None] = None

	class Config:
		orm_mode = True

class UserLogin(BaseModel):
	username: str
	password: str

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	username: Union[str, None] = None