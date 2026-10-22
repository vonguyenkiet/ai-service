import pytest
from pydantic import ValidationError

from supportflow_ai.config import Settings


def test_auth_enabled_by_default_and_no_default_token():
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_staging_cannot_disable_auth():
    with pytest.raises(ValidationError):
        Settings(environment="staging", auth_enabled=False)


def test_production_cannot_disable_auth():
    with pytest.raises(ValidationError):
        Settings(environment="production", auth_enabled=False)


def test_placeholder_token_rejected():
    with pytest.raises(ValidationError):
        Settings(service_token="replace-with-a-long-random-service-token")


def test_invalid_request_budget_rejected():
    with pytest.raises(ValidationError):
        Settings(auth_enabled=False, max_request_bytes=99)
