from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from app.utils import decode_access_token


# oauth2_scheme is what dependencies.py imports.
# It reads the Authorization header, strips "Bearer ",
# and hands the raw token string to get_access_token().
# tokenUrl must match your login endpoint exactly.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/token")


class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request):  # type: ignore
        # Parse Authorization Header
        # Similar to
        # request.header.get("Authorization") ...
        auth_credentials = await super().__call__(request)
        # Access token
        token = auth_credentials.credentials  # type: ignore
        # Validate the token
        token_data = decode_access_token(token)
        # Raise error for invalid token
        if token_data is None:
            raise HTTPException(
                status_code=401,
                detail="Not authorized!",
            )
        # Return token/user data
        return token_data


access_token_bearer = AccessTokenBearer()

# Dependency
AccessTokenDep = Annotated[dict, Depends(access_token_bearer)]
