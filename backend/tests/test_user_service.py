from unittest.mock import patch

from services import user_service


class TestRegisterUser:
    def test_register_success(self):
        with patch("services.user_service.user_repo") as mock_repo:
            mock_repo.exists.return_value = False
            mock_repo.create_user.return_value = {
                "id": 1,
                "username": "newuser",
                "full_name": "New User",
            }

            result = user_service.register_user("newuser", "pass123", "New User")

            assert result.username == "newuser"
            assert result.full_name == "New User"
            call_args = mock_repo.create_user.call_args[0]
            assert call_args[0] == "newuser"
            assert call_args[2] == "New User"

    def test_register_duplicate_raises(self):
        with patch("services.user_service.user_repo") as mock_repo:
            mock_repo.exists.return_value = True

            try:
                user_service.register_user("taken", "pass", "Taken")
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert str(e) == "Username already exists"


class TestVerifyPassword:
    def test_verify_correct_password(self):
        import bcrypt

        hashed = bcrypt.hashpw(b"mypass", bcrypt.gensalt()).decode()
        assert user_service.verify_password("mypass", hashed) is True

    def test_verify_wrong_password(self):
        import bcrypt

        hashed = bcrypt.hashpw(b"correct", bcrypt.gensalt()).decode()
        assert user_service.verify_password("wrong", hashed) is False


class TestGetUser:
    def test_get_existing_user(self):
        with patch("services.user_service.user_repo") as mock_repo:
            mock_repo.get_by_username.return_value = {
                "id": 1,
                "username": "alice",
                "hashed_password": "$2b$...",
                "full_name": "Alice",
            }

            result = user_service.get_user("alice")
            assert result is not None

            assert result["username"] == "alice"
            assert result["full_name"] == "Alice"

    def test_get_missing_user_returns_none(self):
        with patch("services.user_service.user_repo") as mock_repo:
            mock_repo.get_by_username.return_value = None

            result = user_service.get_user("nobody")

            assert result is None
