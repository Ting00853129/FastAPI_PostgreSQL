from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import db
from datetime import timedelta
from schema import UserUpdate, Token
import crud

router = APIRouter(
	prefix="/userinfo",
	tags=["userInfo"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/login")

@router.put("/{username}")
async def update_user(username: str, user_info: UserUpdate, db= Depends(db), token: str = Depends(oauth2_scheme))-> Response:
	user = crud.update_user(db, username, user_info)
	if user:
		return user
	else:
		raise HTTPException(404, crud.error_message('No User found for username {}'.format(username)))
	
@router.get("/{username}")
async def read_user(username: str, db=Depends(db), token: str = Depends(oauth2_scheme)) -> Response:
	user = crud.get_user(db, username)
	if user:
		return user
	else:
		raise HTTPException(404, crud.error_message('No User found for username {}'.format(username)))