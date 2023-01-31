from fastapi import APIRouter
from fastapi import Depends, HTTPException, Response
import crud
from database import db
from schema import UserCreate

router = APIRouter(
	prefix="/user",
	tags=["users"]
)

@router.get("/")
async def read_user(db=Depends(db)) -> Response:
	user = crud.get_user(db)
	if user:
		return user
	else:
		raise HTTPException(404, crud.error_message('No User found.'))
	
@router.post("/")
async def create_user(user:UserCreate, db= Depends(db))-> Response:
	user_info = crud.get_user(db, user.username)
	if user_info:
		raise HTTPException(400, detail = crud.error_message('This username already exists'))
	return crud.create_user(db, user)

@router.delete("/{username}")
async def delete_user(username:str, db= Depends(db))-> Response:
	result = crud.delete_user(db, username)
	if result:
		return {"msg": "Successful"} 
	else:
		raise HTTPException(404,crud.error_message('No user found for username {}'.format(username)))