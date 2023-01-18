from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from main import app
import json

client = TestClient(app)

def test_read_root():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == {"Hello":"World"}


def test_create_user():
	response = client.post("/user",
	json={"username":"test", "password":"test","birthday":"2001-06-22"})
	assert response.status_code == 200
	assert response.json()["birthday"] == "2001-06-22"
	assert response.json()["username"] == "test"

def test_delete_user():
	response = client.delete("/user/test")
	assert response.status_code == 200
	assert response.json() == {"msg":"Successful"}

def test_create_existent_user():
	response = client.post("/user",
	json={"username":"ting", "password":"test","birthday":"2001-06-22"})
	assert response.status_code == 400
	assert response.json() == {"detail": {"error": "This username already exists"}}

def test_delete_nonexistent_user():
	response = client.delete("/user/notfound")
	assert response.status_code == 404
	assert response.json() == {"detail": {"error": "No user found for username notfound"}}

# def test_login():
# 	data = {
# 		"username" : "ting",
# 		"password" : "1234"
# 	}
	
# 	response = client.post("/login", data = json.dumps(data), headers={"content-type": "application/x-www-form-urlencoded"})
# 	assert response.status_code == 200
# 	assert response.json()["token_type"] == "bearer"