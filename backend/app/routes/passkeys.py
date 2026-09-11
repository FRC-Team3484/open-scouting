from datetime import UTC, timedelta, datetime
import os
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from tortoise.timezone import now
from webauthn import base64url_to_bytes, generate_authentication_options, generate_registration_options, verify_authentication_response, verify_registration_response
from webauthn.authentication.verify_authentication_response import VerifiedAuthentication
from webauthn.helpers import options_to_json_dict
from webauthn.helpers.exceptions import InvalidAuthenticationResponse, InvalidRegistrationResponse
from webauthn.helpers.structs import AuthenticatorSelectionCriteria, PublicKeyCredentialDescriptor, ResidentKeyRequirement
from webauthn.registration.verify_registration_response import VerifiedRegistration

from ..dependencies import Identity, require_user
from ..models import Passkey, User, VerificationCode, WebAuthnChallenge
from ..schemas.generic import MessageResponse
from ..schemas.passkeys import PasskeyResponse
from ..utils import IS_DEV
from ..routes.auth import perform_login


# TODO: If the host changes, will all passkeys break?
PASSKEY_RP_ID: str = (
    "localhost"
    if IS_DEV
    else os.getenv(
        "PASSKEY_RP_ID",
        "localhost"
    )
)

router: APIRouter = APIRouter(
    tags=["Passkeys"],
    include_in_schema=IS_DEV
)

@router.post("/passkeys/register/create")
async def create_passkey(response: Response, verification_code_uuid: UUID | None = None, passkey_uuid: UUID | None = None,identity: Identity = Depends(require_user)):
    """
    Begin the passkey registration process

    Requires either verification_code_uuid or passkey_uuid to verify the user's identity, unless the account is less than PASSKEY_NO_VERIFICATION_MINUTES minutes old
    """
    if not identity.user:
        response.status_code = 404
        return MessageResponse(message="User not found")

    if not verification_code_uuid and not passkey_uuid and identity.user.created_at < now() - timedelta(minutes=int(os.getenv("PUBLIC_PASSKEY_NO_VERIFICATION_MINUTES", 15))):
        if not int(os.getenv("PUBLIC_PASSKEY_NO_VERIFICATION_MINUTES", 15)) == -1:
            raise HTTPException(status_code=400, detail="Either verification_code_uuid or passkey_uuid is required")

    if verification_code_uuid:
        verification_code = await VerificationCode.get_or_none(uuid=verification_code_uuid, user=identity.user, verified=True)
        if not verification_code:
            raise HTTPException(status_code=400, detail="Invalid verification code")

    if passkey_uuid:
        passkey = await Passkey.get_or_none(uuid=passkey_uuid, user=identity.user)
        if not passkey:
            raise HTTPException(status_code=400, detail="Invalid passkey")

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
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
        created_by=identity.session
    )

    options_json["challenge_uuid"] = str(challenge.uuid)

    return JSONResponse(content=options_json)

@router.post("/passkeys/register/verify", response_model=MessageResponse)
async def verify_passkey(challenge_uuid: UUID, label: str, response: Response, data: dict = Body(), identity: Identity = Depends(require_user)):
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
        label=label,
        credential_id=verification.credential_id,
        public_key=verification.credential_public_key,
        sign_count=verification.sign_count,
        created_by=identity.session
    )

    await challenge.delete()

    response.status_code = 200
    return MessageResponse(message="Passkey registered")

@router.post("/passkeys/login/create")
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

@router.post("/passkeys/login/verify", response_model=MessageResponse)
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

@router.post("/passkeys/verification/create")
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
        user=user,
    )

    options_json["challenge_uuid"] = str(challenge.uuid)

    return JSONResponse(content=options_json)

@router.post("/passkeys/verification/verify", response_model=MessageResponse)
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

@router.get("/passkeys/get", response_model=list[PasskeyResponse])
async def get_passkeys(identity: Identity = Depends(require_user)):
    """
    Get the passkeys for the current user
    """
    return [
        PasskeyResponse(
            uuid=passkey.uuid,
            label=passkey.label,
            created_at=passkey.created_at
        ) for passkey in await Passkey.filter(user=identity.user)
    ]

@router.delete("/passkeys/delete/{uuid}", response_model=MessageResponse)
async def delete_passkey(uuid: UUID, identity: Identity = Depends(require_user)):
    """
    Delete a passkey on the server

    Parameters:
        uuid (uuid): The uuid of the passkey to delete

    Returns:
        MessageResponse: A message indicating that the passkey was deleted
    """
    passkey_to_delete: Passkey | None = await Passkey.get_or_none(uuid=uuid, user=identity.user)

    if not passkey_to_delete:
        raise HTTPException(status_code=404, detail="Passkey not found")
    else:       
        await passkey_to_delete.delete()
        return MessageResponse(message="Passkey deleted")