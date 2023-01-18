from fastapi import FastAPI,Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from schema import UserUpdate, UserCreate, Token, User, UserLogin
import crud
import models
from typing import Union

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
	"file://wsl.localhost/Ubuntu/home/ting/ncku_practice/frontend/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def db():
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()

@app.get("/")
async def read_root():
	return {"Hello": "World"}


@app.get("/user")
async def read_user(username: Union[str,None] = None, db=Depends(db)) -> Response:
	user = crud.get_user(db, username)
	if user:
		return user
	else:
		raise HTTPException(404, crud.error_message('No User found for username {}'.format(username)))

@app.get("/user/{username}")
async def read_user(username: str, db=Depends(db), token: str = Depends(oauth2_scheme)) -> Response:
	user = crud.get_user(db, username)
	if user:
		return user
	else:
		raise HTTPException(404, crud.error_message('No User found for username {}'.format(username)))

@app.post("/user")
async def create_user(user:UserCreate, db= Depends(db))-> Response:
	user_info = crud.get_user(db, user.username)
	if user_info:
		raise HTTPException(400, detail = crud.error_message('This username already exists'))
	return crud.create_user(db, user)

@app.put("/user/{username}")
async def update_user(username: str, user_info: UserUpdate, db= Depends(db), token: str = Depends(oauth2_scheme))-> Response:
	user = crud.update_user(db, username, user_info)
	if user:
		return user
	else:
		raise HTTPException(404, crud.error_message('No User found for username {}'.format(username)))


@app.delete("/user/{username}")
async def delete_user(username:str, db= Depends(db))-> Response:
	result = crud.delete_user(db, username)
	if result:
		return {"msg": "Successful"} 
	else:
		raise HTTPException(404,crud.error_message('No user found for username {}'.format(username)))

@app.post("/login", response_model= Token)
async def login(db = Depends(db),form_data: OAuth2PasswordRequestForm = Depends())-> Response:
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
