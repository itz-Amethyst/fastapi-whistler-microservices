import secrets
from typing import Optional
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED
from user_service.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.repository.user import UserRepository
from user_service.utils.security.token import decode_access_token

TFA_RECOVERY_ALPHABET = "23456789BCDFGHJKMNPQRTVWXY".lower()  
TFA_RECOVERY_LENGTH = 5 

pwd_context = CryptContext(schemes=[settings.PASSWORD_CRYPT_ALGO], deprecated="auto")

def generate_two_factor_recovery_code():
    return (
        "".join(secrets.choice(TFA_RECOVERY_ALPHABET) for i in range(TFA_RECOVERY_ALPHABET))
        + "-"
        + "".join(secrets.choice(TFA_RECOVERY_ALPHABET) for i in range(TFA_RECOVERY_ALPHABET))
    )
    
# Note the scopes are static here find a better way to make them dynamic
oauth_kwargs = {
    "tokenUrl": "/token/oauth2",
    "scopes": {
        "discount_management": "Create, list or edit discounts",
        "product_management": "Create, list or edit products",
        "full_control": "Full control over what current user has",
    },
}

bearer_description = """Token authorization. Get a token by sending a POST request to `/token` endpoint (JSON-mode, preferred)
or `/token/oauth2` OAuth2-compatible endpoint.
Ensure to use only those permissions that your app actually needs. `full_control` gives access to all permissions of a user
To authorize, send an `Authorization` header with value of `Bearer <token>` (replace `<token>` with your token)
"""
optional_bearer_description = "Same as Bearer, but not required. Logic for unauthorized users depends on current endpoint"

def check_selective_scopes(request, scope, token):
    model_id = request.path_params.get("model_id", None)
    if model_id is None:
        return False
    return f"{scope}:{model_id}" in token.permissions


class AuthDependency(OAuth2PasswordBearer):
    def __init__(self, session: AsyncSession, enabled: bool = True, token_required: bool = True, token: Optional[str] = None, return_token=False):
        self.enabled = enabled
        self.return_token = return_token
        self.token = token
        self.session = session
        super().__init__(
            **oauth_kwargs,
            auto_error=token_required,
            scheme_name="Bearer" if token_required else "BearerOptional",
            description=bearer_description if token_required else optional_bearer_description,
        )

    async def _process_request(self, request: Request, security_scopes: SecurityScopes):
        if not self.enabled:
            if self.return_token:
                return None, None
            return None

        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"

        token: str = self.token if self.token else await super().__call__(request)
        exc = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )

        if not token:
            raise exc

        try:
            decoded_token = decode_access_token(token)
        except ValueError:
            raise exc

        user_id = decoded_token.get("sub")
        scopes = decoded_token.get("scopes", [])

        user_repo = UserRepository(self.session)
        user = await user_repo.get_user_by_id(user_id)

        if not user or not user.is_enabled:
            raise HTTPException(status_code=403, detail="Account is disabled")

        forbidden_exception = HTTPException(
            status_code=403,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

        for scope in security_scopes.scopes:
            if scope not in scopes:
                raise forbidden_exception

        if "server_management" in security_scopes.scopes and not user.is_superuser:
            raise forbidden_exception

        if self.return_token:
            return user, token

        return user

    async def __call__(self, request: Request, security_scopes: SecurityScopes):
        try:
            return await self._process_request(request, security_scopes)
        except HTTPException:
            if self.auto_error:
                raise
            if self.return_token:
                return None, None
            return None
        
auth_dependency = AuthDependency()
optional_auth_dependency = AuthDependency(token_required=False)