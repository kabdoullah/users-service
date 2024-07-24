# import pytest

# def test_login_success(test_client, mock_user_data):
#     response = test_client.post("/api/v1/login", data={"username": mock_user_data.email, "password": "correctpassword"})
#     assert response.status_code == 200
#     response_json = response.json()
    
#     assert "access_token" in response_json
#     assert "refresh_token" in response_json
#     assert response_json["token_type"] == "bearer"

# def test_login_invalid_credentials(test_client):
#     response = test_client.post("/api/v1/login", data={"username": "test@example.com", "password": "wrongpassword"})
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Invalid credentials"}

# def test_login_inactive_user(test_client, mock_user_data):
#     mock_user_data.is_active = False  # Set user to inactive
#     response = test_client.post("/api/v1/login", data={"username": mock_user_data.email, "password": "correctpassword"})
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Inactive user"}
#     mock_user_data.is_active = True  # Reset user to active
