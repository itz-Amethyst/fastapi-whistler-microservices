import secrets
from typing import Optional
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED
from user_service.config import settings

TFA_RECOVERY_ALPHABET = "23456789BCDFGHJKMNPQRTVWXY".lower()  
TFA_RECOVERY_LENGTH = 5 

pwd_context = CryptContext(schemes=[settings.PASSWORD_CRYPT_ALGO], deprecated="auto")

def generate_two_factor_recovery_code():
    return (
        "".join(secrets.choice(TFA_RECOVERY_ALPHABET) for i in range(TFA_RECOVERY_ALPHABET))
        + "-"
        + "".join(secrets.choice(TFA_RECOVERY_ALPHABET) for i in range(TFA_RECOVERY_ALPHABET))
    )

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
    def __init__(self, enabled: bool = True, token_required: bool = True, token: Optional[str] = None, return_token=False):
        self.enabled = enabled
        self.return_token = return_token
        self.token = token
        super().__init__(
            **oauth_kwargs,
            auto_error=token_required,
            scheme_name="Bearer" if token_required else "BearerOptional",
            description=bearer_description if token_required else optional_bearer_description,
        )

    async def _process_request(self, request: Request, security_scopes: SecurityScopes):
        if not self.enabled:
            if self.return_token:  # pragma: no cover
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
        data = (
            await models.User.join(models.Token)
            .select(models.Token.id == token)
            .gino.load((models.User, models.Token))
            .first()
        )
        if data is None:
            raise exc
        user, token = data  # first validate data, then unpack
        await user.load_data()
        if not user.is_enabled:
            raise HTTPException(403, "Account is disabled")
        forbidden_exception = HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
        if "full_control" not in token.permissions:
            for scope in security_scopes.scopes:
                if scope not in token.permissions and not check_selective_scopes(request, scope, token):
                    # add log for this
                    # await run_hook("permission_denied", user, token, scope)
                    raise forbidden_exception
        if "server_management" in security_scopes.scopes and not user.is_superuser:
            # add log for this
            # await run_hook("permission_denied", user, token, "server_management")
            raise forbidden_exception
        # await run_hook("permission_granted", user, token, security_scopes.scopes)
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