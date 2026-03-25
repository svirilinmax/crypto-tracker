# tests/unit/models/test_schemas.py
import pytest
from pydantic import ValidationError

from backend.api_gateway.models.schemas import (
    AssetCreateRequest,
    AssetUpdateRequest,
    UserCreateRequest,
)

@pytest.mark.unit
class TestUserSchemas:
    """Тесты схем пользователей"""

    def test_user_create_valid(self):
        """Валидные данные для создания пользователя"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123!"
        }

        user = UserCreateRequest(**user_data)

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "Password123!"

    def test_user_create_invalid_email(self):
        """Невалидный email"""
        with pytest.raises(ValidationError):
            UserCreateRequest(
                username="testuser",
                email="not-an-email",
                password="Password123!"
            )

    def test_user_create_short_username(self):
        """Слишком короткое имя пользователя"""
        with pytest.raises(ValidationError):
            UserCreateRequest(
                username="ab",  # < 3 символа
                email="test@example.com",
                password="Password123!"
            )


@pytest.mark.unit
class TestAssetSchemas:
    """Тесты схем активов"""

    def test_asset_create_valid(self):
        """Валидное создание актива"""
        asset_data = {
            "symbol": "BTC",
            "min_price": 40000.0,
            "max_price": 50000.0
        }

        asset = AssetCreateRequest(**asset_data)

        assert asset.symbol == "BTC"
        assert asset.min_price == 40000.0
        assert asset.max_price == 50000.0

    def test_asset_create_max_less_than_min(self):
        """max_price должен быть больше min_price"""
        with pytest.raises(ValidationError):
            AssetCreateRequest(
                symbol="BTC",
                min_price=50000.0,
                max_price=40000.0  # меньше min_price!
            )

    def test_asset_create_invalid_symbol_format(self):
        """Символ должен быть в верхнем регистре"""
        with pytest.raises(ValidationError):
            AssetCreateRequest(
                symbol="btc",  # должно быть BTC
                min_price=40000.0,
                max_price=50000.0
            )

    def test_asset_update_partial(self):
        """Обновление только части полей"""
        update_data = {
            "min_price": 42000.0
        }

        asset = AssetUpdateRequest(**update_data)

        assert asset.min_price == 42000.0
        assert asset.max_price is None
        assert asset.symbol is None
