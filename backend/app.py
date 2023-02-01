from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, userInfo
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import db
from datetime import timedelta
from schema import UserUpdate, Token
import crud
app = FastAPI() #create a FastAPI "instance

app.include_router(users.router)
app.include_router(userInfo.router)

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

@app.get("/")
async def read_root():
	return {"Hello": "World"}

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