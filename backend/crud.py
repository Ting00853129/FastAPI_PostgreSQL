from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import schema
import models
from schema import TokenData
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Union

SECRET_KEY = "8c461f46c4b108f2d030759b23ccb94e8a9223094d0a44cf27eca8addf25be7e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user (db: Session, username: str = None):
	if username is None:
		return db.query(models.UserInfo).all()
	else:
		return db.query(models.UserInfo).filter(models.UserInfo.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    setattr(user, "last_login", datetime.utcnow())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(db: Session, username: str, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def  create_user(db: Session, info: schema.UserCreate):
	user_info_model = models.UserInfo(
		username = info.username,
		password = get_password_hash(info.password),
		birthday = info.birthday,
		create_time = datetime.utcnow(),
		last_login = datetime.utcnow()
	)
	db.add(user_info_model)
	db.commit()
	db.refresh(user_info_model)
	return user_info_model

def update_user(db: Session, username: str, info: schema.UserUpdate):
	user_query = get_user(db, username)
	if not user_query:
		raise HTTPException(404, detail="User not found")
	user_data = info.dict(exclude_unset=True)#部分更新
	# for key, value in user_data.items():
	# 	setattr(user_query, key, value)
	if info.password is not None:
		setattr(user_query, "password", get_password_hash(info.password))
	if info.birthday is not None:
		setattr(user_query, "birthday", info.birthday)
	db.add(user_query)
	db.commit()
	db.refresh(user_query)
	return get_user(db, username)
	
def delete_user(db: Session, username: str):
	if get_user(db, username):
		db.query(models.UserInfo).filter(models.UserInfo.username == username).delete()
		db.commit()
		return True
	else :
		return False

def error_message(message):
	return{
		'error': message
	}