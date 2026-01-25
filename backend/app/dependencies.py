from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from .models import User
from .auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await User.get_or_none(uuid=payload.get("sub"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def require_user(
    user: User = Depends(get_current_user),
) -> User:
    return user