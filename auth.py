"""Shared utilities for the Influqa API demo."""

from fastapi import Header, HTTPException, status
from data.sample_data import SAMPLE_USERS


def get_current_user(x_api_key: str = Header(..., alias="X-API-Key")):
    """Validate the API key and return the associated user."""
    user = SAMPLE_USERS.get(x_api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key. Use 'demo_key_brand' or 'demo_key_agency'.",
        )
    return user
