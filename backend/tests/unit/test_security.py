"""tests/unit/test_security.py – Unit tests for JWT and hashing utilities."""
from __future__ import annotations

import pytest
from jose import JWTError

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_is_not_plain(self):
        plain = "MySecret123"
        hashed = hash_password(plain)
        assert hashed != plain

    def test_verify_correct_password(self):
        plain = "MySecret123"
        assert verify_password(plain, hash_password(plain)) is True

    def test_verify_wrong_password(self):
        assert verify_password("wrong", hash_password("correct")) is False


class TestJWT:
    def test_access_token_type(self):
        token = create_access_token("user-id-123")
        payload = decode_token(token)
        assert payload["type"] == "access"
        assert payload["sub"] == "user-id-123"

    def test_refresh_token_type(self):
        token = create_refresh_token("user-id-456")
        payload = decode_token(token)
        assert payload["type"] == "refresh"

    def test_invalid_token_raises(self):
        with pytest.raises(JWTError):
            decode_token("not.a.valid.token")
