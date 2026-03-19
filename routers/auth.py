"""Authentication router for the Influqa API demo."""

from fastapi import APIRouter, Depends
from models import AuthResponse
from auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get(
    "/verify",
    response_model=AuthResponse,
    summary="Verify API Key",
    description=(
        "Verify your API key and retrieve information about the authenticated account. "
        "Pass your API key in the `X-API-Key` header."
    ),
)
def verify_api_key(current_user: dict = Depends(get_current_user)):
    return AuthResponse(
        user_id=current_user["user_id"],
        role=current_user["role"],
        company_name=current_user["company_name"],
        email=current_user["email"],
    )
