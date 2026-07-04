
import os
import re
import secrets
from datetime import UTC, timedelta, datetime
from typing import Literal
from uuid import UUID

from sqlite3 import IntegrityError
from webauthn.helpers.exceptions import InvalidAuthenticationResponse, InvalidRegistrationResponse
from webauthn.registration.verify_registration_response import VerifiedRegistration
from webauthn.authentication.verify_authentication_response import VerifiedAuthentication
from webauthn.helpers import base64url_to_bytes, options_to_json_dict
from webauthn import generate_authentication_options, generate_registration_options, verify_authentication_response, verify_registration_response
from webauthn.helpers.structs import AuthenticatorSelectionCriteria, PublicKeyCredentialDescriptor, ResidentKeyRequirement
from fastapi import APIRouter, Body, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from tortoise.exceptions import FieldError
from tortoise.expressions import Q
from tortoise.timezone import now

from ..utils import IS_DEV
from ..auth import create_access_token, get_password_hash, verify_password
from ..dependencies import Identity, get_identity, require_user, require_superuser

from ..models import Passkey, User, Profile, Settings, Session, VerificationCode, WebAuthnChallenge
from .emails import send_password_change_notification, send_verification_code
from ..schemas.generic import MessageResponse
from ..schemas.auth import BaseSettings, ForgotPasswordRequest, SignupRequest, UserMeResponse, UserResponse, UserSetting, VerifyVerificationCodeRequest, VerifyVerificationCodeResponse


VERIFICATION_CODE_LENGTH = 6
VERIFICATION_CODE_EXPIRE_MINUTES = 15

# Remove the protocol and port from the URL
# TODO: If the host changes, will all passkeys break?
PASSKEY_RP_ID = "localhost" if IS_DEV else re.sub(r"^https?:\/\/|:\d+$", "", os.getenv("PUBLIC_FAST_API_URL", "localhost"))

router: APIRouter = APIRouter(
    tags=["Auth"],
    include_in_schema=IS_DEV
)

def field_type_to_string(type: str) -> Literal["string", "number", "boolean", "array", "json"]:
    if type == "StringSetting":
        return "string"
    elif type == "NumberSetting":
        return "number"
    elif type == "BooleanSetting":
        return "boolean"
    elif type == "ArraySetting":
        return "array"
    elif type == "JSONSetting":
        return "json"
    else:
        return "json"

@router.get("/auth/me", response_model=UserMeResponse)
async def me(
    identity: Identity = Depends(get_identity)
):
    """
    Validates the current user, and returns their details

    Returns:
        UserMeResponse: The current user details, and whether they are authenticated or not
    """

    if identity.user:
        user = UserResponse(
            uuid=identity.user.uuid,
            username=identity.user.username,
            email=identity.user.email,
            is_superuser=identity.user.is_superuser,
            display_name=identity.profile.display_name,
            team_number=identity.profile.team_number,
            email_verified=identity.user.email_verified,
            profile_picture_url=identity.profile.profile_picture_url,
            created_at=identity.user.created_at
        )

        settings = await Settings.get_or_none(user=identity.user)
        settings_list: list[UserSetting] | None = []

        if settings:
            for key, field in Settings._meta.fields_map.items():
                if key in {"user", "uuid"}:
                    continue

                if key.endswith("_id"):
                    continue
                    
                settings_list.append(
                    UserSetting(
                        key=key,
                        value=getattr(settings, key),
                        name=field.display_name,
                        description=field.setting_description,
                        section=field.section,
                        visible=field.visible,
                        type=field_type_to_string(field.__class__.__name__),
                    )
                )

    else:
        user = None
        settings_list = None

    return UserMeResponse(
        authenticated=identity.user is not None,
        user=user,
        settings=settings_list
    )

async def perform_login(
    request: Request, 
    response: Response, 
    passkey_user: User | None = None, 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    if passkey_user:
        user = passkey_user
    else:
        user = await User.get_or_none(
            Q(
                username=form_data.username,
                email=form_data.username,
                join_type=Q.OR
            )
        )

        if not verify_password(
            form_data.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    session_id = request.cookies.get("session_id")

    session = None

    if session_id:
        session = await Session.get_or_none(
            uuid=session_id
        )

    if not session:
        session = await Session.create(
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )

    session.user = user
    await session.save()

    access_token = create_access_token(
        {
            "sub": str(user.uuid),
            "sid": str(session.uuid)
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not IS_DEV,  # False for local dev only
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    response.set_cookie(
        key="session_id",
        value=str(session.uuid),
        httponly=True,
        secure=not IS_DEV,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )

    return MessageResponse(message="Login successful")

@router.post("/auth/login", response_model=MessageResponse)
async def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Logs in a user

    Returns:
        MessageResponse: A message indicating that the user has been logged in
    """
    return await perform_login(request, response, form_data=form_data)

@router.post("/auth/signup", response_model=MessageResponse)
async def signup(
    request: Request,
    response: Response,
    data: SignupRequest
):
    """
    Create a new user

    If this is the first user on the server, make them a superuser

    TODO: email_verified status probably shouldn't come from the client, and should instead be verified by the server to prevent verified spoofing

    Paramaters:
        data (SignupRequest): The data to create the user

    Returns:
        MessageResponse: A message indicating that the user has been created
    """
    # Ensure that the verification code has been verified
    email_verified = False
    if data.email and data.verification_code_uuid:
        verification_code = await VerificationCode.get_or_none(uuid=data.verification_code_uuid, email=data.email, verified=True)
        if verification_code:
            email_verified = True
        else:
            email_verified = False

    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password: str = get_password_hash(data.password)

    try:
        user: User = await User.create(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password,
            email_verified=email_verified
        )
        await Profile.create(user=user, display_name=data.display_name, team_number=int(data.team_number))

        # If this is the first user on the server, make them a superuser
        if await User.all().count() == 1:
            user.is_superuser = True
            await user.save()
            print(f"User {user.username} is now a superuser, because this is the first user on the server")

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user: User | None = await User.get_or_none(username=data.username)

    session = await Session.create(
        user=user,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

    access_token = create_access_token(
        {
            "sub": str(user.uuid),
            "sid": str(session.uuid)
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=IS_DEV,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    response.set_cookie(
        key="session_id",
        value=str(session.uuid),
        httponly=True,
        secure=IS_DEV,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )

    return MessageResponse(message="Signup successful")

@router.post("/auth/logout", response_model=MessageResponse)
async def logout(response: Response):
    """
    Logs out a user
    """

    response.delete_cookie("access_token", path="/")
    response.delete_cookie("session_id", path="/")

    return MessageResponse(message="Logout successful")

@router.get("/users/", response_model=list[UserResponse])
async def get_users(identity: Identity = Depends(require_superuser)) -> list[UserResponse]:
    """
    Get all users on the server

    Requires superuser access

    Returns:
        list[User]: A list of all users
    """
    user_list: list[UserResponse] = []
    users: list[User] = await User.all()

    for user in users:
        profile = await Profile.get_or_none(user=user)

        if profile:
            user_list.append(
                UserResponse(
                    uuid=user.uuid,
                    username=user.username,
                    email=user.email,
                    is_superuser=user.is_superuser,
                    display_name=profile.display_name,
                    team_number=profile.team_number,
                    email_verified=user.email_verified,
                    profile_picture_url=profile.profile_picture_url,
                    created_at=user.created_at
                )
            )
        else:
            print(f"WARN: User {user.username} ({user.uuid}) has no profile")
            user_list.append(
                UserResponse(
                    uuid=user.uuid,
                    username=user.username,
                    email=user.email,
                    is_superuser=user.is_superuser,
                    display_name=None,
                    team_number=0,
                    email_verified=user.email_verified,
                    profile_picture_url=None,
                    created_at=user.created_at
                )
            )

    return user_list

@router.delete("/users/delete/{uuid}", response_model=MessageResponse)
async def delete_user(uuid: UUID, identity: Identity = Depends(require_user)) -> dict[str, str]:
    """
    Delete a user on the server

    Requires superuser access

    Parameters:
        uuid (uuid): The uuid of the user to delete

    Returns:
        MessageResponse: A message indicating that the user was deleted
    """
    user_to_delete: User | None = await User.get_or_none(uuid=uuid)

    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        # Only be able to delete user if they are deleting themselves, or if they are a superuser
        if user_to_delete.uuid == identity.user.uuid or identity.user.is_superuser:        
            await user_to_delete.delete()
            return {"message": "User deleted"}
        else:
            raise HTTPException(status_code=403, detail="User not authorized to delete this user")

@router.get("/users/me/get_settings", response_model=list[UserSetting])
async def get_user_settings(identity: Identity = Depends(require_user)) -> list[UserSetting]:
    """
    Get the settings for the current user

    Returns:
        BaseSettings: The settings for the current user
    """
    settings: Settings | None = await Settings.get_or_none(user=identity.user)
    settings_list: list[UserSetting] | None = []        

    if not settings:
        settings = await Settings.create(user=identity.user)

    for key, field in Settings._meta.fields_map.items():
        if key in {"user", "uuid"}:
            continue

        if key.endswith("_id"):
            continue
            
        settings_list.append(
            UserSetting(
                key=key,
                value=getattr(settings, key),
                name=field.display_name,
                description=field.setting_description,
                section=field.section,
                visible=field.visible,
                type=field_type_to_string(field.__class__.__name__),
            )
        )

    return settings_list

@router.post("/users/me/update_settings", response_model=BaseSettings)
async def update_user_settings(data: BaseSettings, identity: Identity = Depends(require_user)) -> Settings:
    """
    Update the settings for the current user

    Parameters:
        data (BaseSettings): The settings to update

    Returns:
        BaseSettings: The settings for the current user
    """
    settings: Settings | None = await Settings.get_or_none(user=identity.user)

    if not settings:
        settings = await Settings.create(user=identity.user)

    updates = data.model_dump(exclude_unset=True)

    try:
        for key, value in updates.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
            else:
                print(f"Warning: ignoring unknown setting key '{key}'")

        await settings.save()
    except FieldError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return settings

@router.post("/users/set_superuser/{uuid}", response_model=MessageResponse)
async def set_superuser(uuid: UUID, identity: Identity = Depends(require_superuser)) -> MessageResponse:
    """
    Set a user as a superuser

    Requires superuser access

    Parameters:
        uuid (uuid): The uuid of the user to set as a superuser

    Returns:
        User: The user that was set as a superuser
    """
    user_to_set_superuser: User | None = await User.get_or_none(uuid=uuid)

    if not user_to_set_superuser:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        user_to_set_superuser.is_superuser = True
        await user_to_set_superuser.save()
        return MessageResponse(message="User set as superuser")

@router.post("/users/remove_superuser/{uuid}", response_model=MessageResponse)
async def remove_superuser(uuid: UUID, identity: Identity = Depends(require_superuser)) -> MessageResponse:
    """
    Remove a user as a superuser

    Requires superuser access

    Parameters:
        uuid (uuid): The uuid of the user to remove as a superuser

    Returns:
        User: The user that was removed as a superuser
    """
    user_to_remove_superuser: User | None = await User.get_or_none(uuid=uuid)

    if not user_to_remove_superuser:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        user_to_remove_superuser.is_superuser = False
        await user_to_remove_superuser.save()
        return MessageResponse(message="User removed as superuser")

@router.post("/users/me/set_display_name", response_model=MessageResponse)
async def set_display_name(display_name: str, identity: Identity = Depends(require_user)) -> MessageResponse:
    """
    Set the display name for the current user

    Parameters:
        display_name (str): The display name to set

    Returns:
        MessageResponse: A message indicating that the display name was set
    """
    profile: Profile | None = await Profile.get_or_none(user=identity.user)

    if not profile:
        profile = await Profile.create(user=identity.user)

    profile.display_name = display_name
    await profile.save()

    return MessageResponse(message="Display name set")

@router.post("/users/me/set_team_number", response_model=MessageResponse)
async def set_team_number(team_number: int, identity: Identity = Depends(require_user)) -> MessageResponse:
    """
    Set the team number for the current user

    Parameters:
        team_number (int): The team number to set

    Returns:
        MessageResponse: A message indicating that the team number was set
    """
    profile: Profile | None = await Profile.get_or_none(user=identity.user)

    if not profile:
        profile = await Profile.create(user=identity.user)

    profile.team_number = team_number
    await profile.save()

    return MessageResponse(message="Team number set")

@router.get("/auth/check_unique_username")
async def check_unique_username(username: str, email: str) -> JSONResponse:
    """
    Check if a username and email is unique

    Parameters:
        username (str): The username to check
        email (str): The email to check

    Returns:
        MessageResponse: A message indicating whether the username is unique
    """
    username_check = await User.get_or_none(username=username)
    email_check = await User.get_or_none(email=email)

    if username_check:
        return JSONResponse(content={"message": "There is already a user associated with this username"}, status_code=409)
    elif email_check:
        return JSONResponse(content={"message": "There is already a user associated with this email"}, status_code=409)
    else:
        return JSONResponse(content={"message": "Username and email are unique"}, status_code=200)

@router.post("/auth/create_verification_code")
async def create_verification_code(email: str, style: Literal["verification_code", "forgot_password"] = "verification_code", identity: Identity = Depends(get_identity)) -> JSONResponse:
    """
    Given an email, create a verification code and send it to the user

    If an identity is found, attach the user to the verification code

    Parameters:
        email (str): The email to create a verification code for
    """

    def create_verification_code(length: int = 6) -> str:
        """
        Returns a random digit number of length

        Since randbelow returns an int under the specified length, 
            :06d is the format for length digits, adding a 
            zero in front if the number is less than the length
        """
        return f"{secrets.randbelow(10**length):0{length}d}"

    if os.getenv("PUBLIC_EMAIL_ENABLED", "false") == "true":
        code = VerificationCode(
            user=identity.user,
            code=create_verification_code(VERIFICATION_CODE_LENGTH),
            email=email,
            verified=False
        )

        await code.save()

        return await send_verification_code(email, code.code, style)
    else:
        return JSONResponse(content={"message": "emails are disabled"}, status_code=403)
    

@router.post("/auth/verify_verification_code", response_model=VerifyVerificationCodeResponse)
async def verify_verification_code(data: VerifyVerificationCodeRequest, response: Response, identity: Identity = Depends(get_identity)):
    """
    Verify a verification code for a user

    Given an email and a verification code, verify the verification code

    If an identity is found, the verification code must be attached to the user to be validated.
        This would occour when verifying an email from the profile page when their email was not yet verified.
        When doing this, also set that user's email_verified to be true if it is not already.

    The code's created_at should be less than VERIFICATION_CODE_EXPIRE_MINUTES to be validated.

    Parameters:
        email (str): The email to verify the verification code for
        code (int): The verification code to verify
    """

    if (identity.user):
        verification_code = await VerificationCode.get_or_none(user=identity.user, code=data.code, email=data.email, verified=False)
    else:
        verification_code = await VerificationCode.get_or_none(code=data.code, email=data.email, verified=False)

    if not verification_code:
        response.status_code = 400
        return VerifyVerificationCodeResponse(verified=False, message="Verification code not found")

    elif verification_code.created_at < now() - timedelta(minutes=VERIFICATION_CODE_EXPIRE_MINUTES):
        response.status_code = 400
        return VerifyVerificationCodeResponse(verified=False, message="Verification code expired")

    else:
        verification_code.verified = True

        if (identity.user):
            identity.user.email_verified = True
            await identity.user.save()
        await verification_code.save()

        response.status_code = 200
        return VerifyVerificationCodeResponse(verified=False, message="Verification code verified", verification_code_uuid=verification_code.uuid)

@router.post("/auth/forgot_password", response_model=MessageResponse)
async def forgot_password(data: ForgotPasswordRequest, response: Response):
    """
    Given an email, password, and verification code UUID, change the password for a user

    First, confirm that the verification code is valid. If so, change the password for the user.

    Parameters:
        email (str): The email to change the password for
        password (str): The new password
        verification_code_uuid (str): The UUID of the verification code
    """
    verification_code = VerificationCode.get_or_none(uuid=data.verification_code_uuid, email=data.email, verified=True)
    if not verification_code:
        response.status_code = 400
        return MessageResponse(message="Invalid verification code")

    user = await User.get_or_none(email=data.email)
    if not user:
        response.status_code = 404
        return MessageResponse(message="User not found")

    user.hashed_password = get_password_hash(data.password)
    await user.save()

    _ = await send_password_change_notification(data.email, user.username)

    response.status_code = 200
    return MessageResponse(message="Password changed")

# Passkeys
@router.post("/auth/passkeys/register/create")
async def create_passkey(response: Response, identity: Identity = Depends(require_user)):
    """
    Begin the passkey registration process
    """
    if not identity.user:
        response.status_code = 404
        return MessageResponse(message="User not found")

    options = generate_registration_options(
        rp_id=PASSKEY_RP_ID,
        rp_name="Open Scouting",
        user_name=identity.user.username,
        user_id=identity.user.uuid.bytes,
        user_display_name=identity.profile.display_name,
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.PREFERRED,
        ),
        exclude_credentials=[
            PublicKeyCredentialDescriptor(
                id=pk.credential_id
            )
            for pk in await Passkey.filter(user=identity.user)
        ]
    )

    options_json =  options_to_json_dict(options)

    challenge = await WebAuthnChallenge.create(
        challenge=options.challenge,
        user=identity.user,
        expires_at=datetime.now(UTC) + timedelta(minutes=5)
    )

    options_json["challenge_uuid"] = str(challenge.uuid)

    return JSONResponse(content=options_json)

@router.post("/auth/passkeys/register/verify", response_model=MessageResponse)
async def verify_passkey(challenge_uuid: UUID, response: Response, data: dict = Body(), identity: Identity = Depends(require_user)):
    """
    Verify the passkey registration
    """
    try:
        challenge: WebAuthnChallenge | None = await WebAuthnChallenge.get_or_none(
            uuid=challenge_uuid
        )

        if challenge is None:
            response.status_code = 400
            return MessageResponse(message="No challenge found")

        if challenge.expires_at < datetime.now(UTC):
            response.status_code = 400
            return MessageResponse(message="Challenge expired")

        verification: VerifiedRegistration = verify_registration_response(
            credential=data,
            expected_challenge=challenge.challenge,
            expected_rp_id=PASSKEY_RP_ID,
            expected_origin=os.getenv("PUBLIC_FRONTEND_URL", "http://localhost:5173"),
        )
    except InvalidRegistrationResponse as e:
        response.status_code = 400
        return MessageResponse(message=f"Invalid registration response {e}")

    _ = await Passkey.create(
        user=identity.user,
        credential_id=verification.credential_id,
        public_key=verification.credential_public_key,
        sign_count=verification.sign_count,
    )

    await challenge.delete()

    response.status_code = 200
    return MessageResponse(message="Passkey registered")

@router.post("/auth/passkeys/login/create")
async def create_login_passkey(response: Response):
    """
    Begin the passkey login process
    """
    options = generate_authentication_options(
        rp_id=PASSKEY_RP_ID
    )

    options_json =  options_to_json_dict(options)

    challenge = await WebAuthnChallenge.create(
        challenge=options.challenge,
        expires_at=datetime.now(UTC) + timedelta(minutes=5)
    )

    options_json["challenge_uuid"] = str(challenge.uuid)

    return JSONResponse(content=options_json)

@router.post("/auth/passkeys/login/verify", response_model=MessageResponse)
async def verify_login_passkey(challenge_uuid: UUID, request: Request, response: Response, data: dict = Body()):
    """
    Verify the passkey login
    """
    try:
        challenge: WebAuthnChallenge | None = await WebAuthnChallenge.get_or_none(
            uuid=challenge_uuid
        )

        if challenge is None:
            response.status_code = 400
            return MessageResponse(message="No challenge found")

        if challenge.expires_at < datetime.now(UTC):
            response.status_code = 400
            return MessageResponse(message="Challenge expired")

        credential_id = base64url_to_bytes(data["rawId"])

        passkey = await Passkey.get_or_none(
            credential_id=credential_id
        ).prefetch_related("user")

        if passkey is None:
            response.status_code = 400
            return MessageResponse(message="Passkey not found")

        verification: VerifiedAuthentication = verify_authentication_response(
            credential=data,
            expected_challenge=challenge.challenge,
            expected_rp_id=PASSKEY_RP_ID,
            expected_origin=os.getenv("PUBLIC_FRONTEND_URL", "http://localhost:5173"),
            credential_public_key=passkey.public_key,
            credential_current_sign_count=passkey.sign_count
        )

        await challenge.delete()

        if verification.user_verified:
            return await perform_login(request, response, passkey.user)

        else:
            response.status_code = 400
            return MessageResponse(message="User not verified")
    except InvalidAuthenticationResponse:
        response.status_code = 400
        return MessageResponse(message="Invalid authentication response")

@router.post("/auth/passkeys/verification/create")
async def create_verification_passkey(email: str, response: Response):
    """
    Begin the passkey verification process
    """
    user = await User.get_or_none(email=email)
    if not user:
        response.status_code = 404
        return MessageResponse(message="User not found")

    options = generate_authentication_options(
        rp_id=PASSKEY_RP_ID,
    )

    options_json =  options_to_json_dict(options)

    challenge = await WebAuthnChallenge.create(
        challenge=options.challenge,
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
        user=user
    )

    options_json["challenge_uuid"] = str(challenge.uuid)

    return JSONResponse(content=options_json)

@router.post("/auth/passkeys/verification/verify", response_model=MessageResponse)
async def verify_verification_passkey(challenge_uuid: UUID, email: str, request: Request, response: Response, data: dict = Body()):
    """
    Verify the passkey verification
    """
    try:
        user = await User.get_or_none(email=email)
        if not user:
            response.status_code = 404
            return MessageResponse(message="User not found")

        challenge: WebAuthnChallenge | None = await WebAuthnChallenge.get_or_none(
            uuid=challenge_uuid,
            user=user
        )

        if challenge is None:
            response.status_code = 400
            return MessageResponse(message="No challenge found")

        if challenge.expires_at < datetime.now(UTC):
            response.status_code = 400
            return MessageResponse(message="Challenge expired")

        credential_id = base64url_to_bytes(data["rawId"])

        passkey = await Passkey.get_or_none(
            credential_id=credential_id,
            user=user
        ).prefetch_related("user")

        if passkey is None:
            response.status_code = 400
            return MessageResponse(message="Passkey not found")

        verification: VerifiedAuthentication = verify_authentication_response(
            credential=data,
            expected_challenge=challenge.challenge,
            expected_rp_id=PASSKEY_RP_ID,
            expected_origin=os.getenv("PUBLIC_FRONTEND_URL", "http://localhost:5173"),
            credential_public_key=passkey.public_key,
            credential_current_sign_count=passkey.sign_count
        )

        await challenge.delete()

        if verification.user_verified:
            return JSONResponse(content={"message": "User verified", "passkey_uuid": str(passkey.uuid)})

        else:
            response.status_code = 400
            return MessageResponse(message="User not verified")
    except InvalidAuthenticationResponse:
        response.status_code = 400
        return MessageResponse(message="Invalid authentication response")