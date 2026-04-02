

def test_success_user_registration(client):
    response = client.post(
        "/api/auth/registration",
        json={"email": "example238@gmail.com", "username": "my_username", "password": "my_password"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data is not None
    assert data["user"]["username"] == "my_username"
    assert data["access_token"] is not None
    assert data["refresh_token"] is not None
    assert data["token_type"] == "bearer"

def test_unsuccess_user_registration(client):
    client.post(
        "/api/auth/registration",
        json={"email": "example238@gmail.com", "username": "my_username", "password": "my_password"},
    )

    response = client.post(
        "/api/auth/registration",
        json={"email": "example238@gmail.com", "username": "my_username", "password": "my_password"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "User already exists"

def test_success_user_login(client):
    register_response = client.post(
        "/api/auth/registration",
        json={"email": "example238@gmail.com", "username": "my_username", "password": "my_password"},
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/api/auth/login",
        json={"email": "example238@gmail.com", "username": "my_username", "password": "my_password"}
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert data is not None
    assert data["user"]["username"] == "my_username"
    assert data["access_token"] is not None
    assert data["refresh_token"] is not None
    assert data["token_type"] == "bearer"