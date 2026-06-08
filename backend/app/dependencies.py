from dataclasses import dataclass
from datetime import datetime
from fastapi import Depends, HTTPException, Request, Response

from .utils import IS_DEV

from .models import Session, User
from .auth import decode_access_token

@dataclass
class Identity:
    user: User | None
    session: Session | None

async def get_identity(request: Request, response: Response) -> Identity:
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
    else:
        session.last_seen = datetime.now()
        await session.save()

    # Set session cookie
    response.set_cookie(
        key="session_id",
        value=str(session.uuid),
        httponly=True,
        secure=not IS_DEV,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
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

async def require_user(identity: Identity = Depends(get_identity)) -> Identity:
    """
    Requires a user to be logged in

    Otherwise, throws a 401 error

    Returns:
        Identity: The current user
    """
    if identity.user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    return identity

async def require_superuser(identity: Identity = Depends(get_identity)) -> Identity:
    """
    Requires a superuser to be logged in, and a superuser

    Otherwise, throws a 401 if not logged in, or a 403 if not a superuser

    Returns:
        Identity: The current user
    """
    print(identity)
    if identity.user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
        
    if not identity.user.is_superuser:
        raise HTTPException(status_code=403, detail="Superuser required")

    return identity