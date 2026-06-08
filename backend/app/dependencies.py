from dataclasses import dataclass
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from .models import Session, User
from .auth import decode_access_token

@dataclass
class Identity:
    user: User | None
    session: Session | None

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

async def require_superuser(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Superuser required")
    return user

async def get_identity(request: Request) -> Identity:
    """
    Returns the current user and session from the request cookies

    Used as a dependency for routes that require authentication or session data

    Returns:
        Identity: The current user and session
    """

    session: Session | None = None
    user: User | None = None

    # Load session
    session_id = request.cookies.get("session_id")

    if session_id:
        session = await Session.get_or_none(uuid=session_id)


    # Load auth token
    token = request.cookies.get("access_token")

    print(request.cookies)
    if token:
        payload = decode_access_token(token)

        if payload:
            user_id = payload.get("sub")

            if user_id:
                user = await User.get_or_none(uuid=user_id)

                # If user doesn't exist anymore, treat as logged out
                # but don't error the request
                if not user:
                    user = None

    # Create session if missing
    if session is None:
        session = await Session.create(
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            user=None
        )

    # Attach user to session
    if user and session.user_id != user.uuid:
        session.user = user
        await session.save()

    # Return identity
    return Identity(
        user=user,
        session=session
    )