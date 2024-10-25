from src.test.conftest import client


def test_registration():
    # Тестирование endpoint для регистрации

    response_to_create_client = client.post(
        url="http://localhost:8000/api/v1/auth/registration",
        json={
            "email_user": "user@example.com",
            "password_user": "test12345",
            "name_user": "gogop",
            "surname_user": "sklyarov",
            "main_name_user": "string",
            "date_registration": "2024-10-25",
        },
    )

    assert (
        response_to_create_client.status_code == 201
    ), "Не удалось создать пользователя"


def test_auth_user():
    # Тестирование endpoint для авторизации пользователя

    response_to_auth = client.post(
        url="http://localhost:8000/api/v1/auth/login",
        data={"username": "user@example.com", "password": "test12345"},
    )

    assert response_to_auth.status_code == 200
