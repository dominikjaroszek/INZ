from app.services.userService import *
from app.models.user import User

from types import SimpleNamespace
import json

def test_check_password_controller(setup_database_user):
    user = get_user_by_email("john.doe@example.com")
    assert check_password_controller(user, "Password1!") == True

def test_get_user_by_email(setup_database_user):
    user = get_user_by_email("john.doe@example.com")
    assert user is not None
    assert user.firstName == "John"

def test_get_user_by_id(setup_database_user):
    user = get_user_by_id(2)
    assert user is not None
    assert user.firstName == "John2"


def test_change_password(setup_database_user):
    user = get_user_by_id(2)
    data = SimpleNamespace(newPassword="Password3!")
    assert change_password(data, user) == True
                             


def test_register_user(test_client, setup_database_user):
    data = {
        "firstName": "Test",
        "lastName": "User",
        "email": "test.user@example.com",
        "password": "Password1!"  # Spełnia kryteria walidacji hasła
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = test_client.post("/register", data=json.dumps(data), headers=headers)
    
    # Dodanie logowania odpowiedzi serwera w przypadku niepowodzenia testu
    if response.status_code != 201:
        print(f"Response data: {response.data}")
    
    assert response.status_code == 201
    assert response.json["message"] == "User created!"


def test_change_password_controller_succesfully(test_client, setup_database_user, get_token):
    headers = {
        "x-access-tokens": get_token,
        'Content-Type': 'application/json'
    }
    data = {
        "oldPassword": "Password1!",
        "newPassword": "Password2!",
    }
    response = test_client.patch("/user/change_password", data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.json["message"] == "Password changed successfully"

def test_change_password_controller_the_same_password(test_client, setup_database_user, get_token):
    headers = {
        "x-access-tokens": get_token,
        'Content-Type': 'application/json'
    }
    data = {
        "oldPassword": "Password1!",
        "newPassword": "Password1!",
    }
    response = test_client.patch("/user/change_password", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["message"] == "The new password must be used over the old one"

def test_change_password_controller_wrong_old_password(test_client, setup_database_user, get_token):
    headers = {
        "x-access-tokens": get_token,
        'Content-Type': 'application/json'
    }
    data = {
        "oldPassword": "Password2!",
        "newPassword": "Password3!",
    }
    response = test_client.patch("/user/change_password", data=json.dumps(data), headers=headers)
    assert response.status_code == 401
    assert response.json["message"] == "Wrong password"



def test_get_contact(test_client, setup_database_user, get_token):
    headers = {
        "x-access-tokens": get_token
    }
    response = test_client.get("/contact", headers=headers)
    assert response.status_code == 200

