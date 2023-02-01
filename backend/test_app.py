from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
token = ''

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

def test_create_existent_user():
	response = client.post("/user",
	json={"username":"ting", "password":"test","birthday":"2001-06-22"})
	assert response.status_code == 400
	assert response.json() == {"detail": {"error": "This username already exists"}}

def test_login():
	data = {
		'username' : 'test',
		'password' : 'test'
	}
	
	response = client.post("/login",
		data = data,
	 	headers={
			"content-type": "application/x-www-form-urlencoded"
			}
		)
	assert response.status_code == 200
	assert len(response.json()['access_token']) > 0
	token = response.json()['access_token']
	assert response.json()['token_type'] == 'bearer'

def test_get_user_info_with_token():
	response = client.get('/userinfo/test',
		headers={
			'Authorization': f'Bearer {token}'
		}
	)
	assert response.status_code == 200
	assert response.json()['username'] == 'test'

def test_get_user_info_without_token():
	response = client.get('/userinfo/test')
	assert response.status_code == 401
	assert response.json()['detail'] == 'Not authenticated'

def test_update_birthday():
	response = client.put(
		'/userinfo/test',
		json = {'birthday': '2020-01-01'},
		headers={
			'Authorization': f'Bearer {token}'
		}
	)
	assert response.status_code == 200
	assert response.json()['username'] == 'test'
	assert response.json()['birthday'] == '2020-01-01'

def test_update_password():
	response = client.put(
		'/userinfo/test',
		json = {'password': 'newpassword'},
		headers={
			'Authorization': f'Bearer {token}'
		}
	)
	assert response.status_code == 200
	assert response.json()['username'] == 'test'

def test_update_birthday_and_password():
	response = client.put(
		'/userinfo/test',
		json = {'birthday': '2020-01-01','password': 'newpassword'},
		headers={
			'Authorization': f'Bearer {token}'
		}
	)
	assert response.status_code == 200
	assert response.json()['username'] == 'test'
	assert response.json()['birthday'] == '2020-01-01'

def test_delete_nonexistent_user():
	response = client.delete("/user/notfound")
	assert response.status_code == 404
	assert response.json() == {"detail": {"error": "No user found for username notfound"}}

def test_delete_user():
	response = client.delete("/user/test")
	assert response.status_code == 200
	assert response.json() == {"msg":"Successful"}