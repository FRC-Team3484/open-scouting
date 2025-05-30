from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from . import email
from authentication.models import Profile, VerificationCode
from main.views import index

import random
from datetime import timedelta
import json


def generate_verification_code(length=6):
    verification_code = ""
    for i in range(length):
        verification_code += str(random.randint(0, 9))
    return verification_code


def auth(request):
    if request.user.is_authenticated:
        response = index(request)
        return response

    else:
        context = {
            "SERVER_IP": settings.SERVER_IP,
            "TBA_API_KEY": settings.TBA_API_KEY,
            "SERVER_MESSAGE": settings.SERVER_MESSAGE,
            "EMAIL_HOST_USER": settings.EMAIL_HOST_USER,
            "EMAIL_ENABLED": settings.EMAIL_ENABLED,
        }

        return render(request, "authentication.html", context)


def profile(request):
    """
    Returns the profile page
    """
    if request.user.is_authenticated:
        context = {
            "SERVER_IP": settings.SERVER_IP,
            "TBA_API_KEY": settings.TBA_API_KEY,
            "SERVER_MESSAGE": settings.SERVER_MESSAGE,
            "EMAIL_ENABLED": settings.EMAIL_ENABLED,
            "user": request.user,
        }

        return render(request, "profile.html", context)
    else:
        return redirect("auth")


def sign_in(request):
    """
    Signs the user in using the provided email and password and authenticates the session

    Body Parameters:
        email: The email of the user
        password: The password of the user

    Returns:
        Redirects to the home page if the user is authenticated and returns 'error' otherwise
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        try:
            user = authenticate(
                request,
                username=body["email"],
                password=body["password"],
            )

            if user is not None:
                login(request, user)
                return HttpResponse("success", status=200)
            else:
                return HttpResponse("incorrect_credentials", status=401)
        except Exception:
            return HttpResponse("error", status=500)

    else:
        return HttpResponse("Request is not a POST request!", status=501)


def sign_out(request):
    """
    Signs the user out of the session
    """
    if request.method == "POST":
        logout(request)
        return HttpResponse("success", status=200)
    else:
        return HttpResponse("Request is not a POST request!", status=501)


def forgot_password(request):
    """
    Sends the user a verification code to their email for resetting their password

    Body Parameters:
        email: The email the user provided which the verification code should be sent to

    Returns:
        expires: The expiration date and time of the code
        user_uuid: The uuid of the user generated on the client
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        user = User.objects.filter(email=body["email"]).first()
        if not user:
            return HttpResponse("user_not_found", status=404)

        code = generate_verification_code()
        code_expires = timezone.now() + timedelta(minutes=10)

        code_object = VerificationCode(
            code=code,
            created=timezone.now(),
            expires=code_expires,
            user_uuid=user.id,
        )
        code_object.save()

        email.send_change_password([body["email"]], user.profile.display_name, code)

        return JsonResponse(
            {
                "expires": code_expires,
                "user_uuid": user.id,
            },
            safe=False,
        )

    else:
        return HttpResponse("Request is not a POST request!", status=501)


def change_password(request):
    """
    Changes the password of the user to a new one, only possible if the provided verification code is valid

    Body Parameters:
        code: The verification code provided from the client
        user_uuid: The uuid of the user from the client. If unsafe, this should be the user's email instead
        password: The password the user is setting
        unsafe: Weather or not to check if the code is valid (used when emails are disabled on the server)
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        if body["unsafe"]:
            user = User.objects.filter(email=body["user_uuid"]).first()
            user.set_password(body["password"])
            user.save()
            return HttpResponse("success", status=200)

        code_object = VerificationCode.objects.filter(
            code=body["code"], user_uuid=body["user_uuid"], verified=True
        ).first()

        if code_object:
            user = User.objects.filter(id=code_object.user_uuid).first()
            user.set_password(body["password"])
            user.save()
            return HttpResponse("success", status=200)

        else:
            return HttpResponse("does_not_exist", status=401)

    else:
        return HttpResponse("Request is not a POST request!", status=501)


def send_verification_code(request):
    """
    Generate and send a verification code to the user

    Body Parameters:
        uuid: The uuid of the user generated on the client
        email: The email the user provided which the verification code should be sent to
        display_name: The provided display name of the user

    Returns:
        expires: The expiration date and time of the code
        user_uuid: The uuid of the user generated on the client
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        code = generate_verification_code()
        code_expires = timezone.now() + timedelta(minutes=10)

        code_object = VerificationCode(
            code=code,
            created=timezone.now(),
            expires=code_expires,
            user_uuid=body["uuid"],
        )
        code_object.save()

        email.send_verify([body["email"]], body["display_name"], code)

        return JsonResponse(
            {
                "expires": code_expires,
                "user_uuid": body["uuid"],
            },
            safe=False,
        )

    else:
        return HttpResponse("Request is not a POST request!", status=501)


def check_verification_code(request):
    """
    Check a verification code the user entered on the client

    Body Parameters:
        code: The verification code provided from the client
        user-uuid: The uuid of the user generated on the client

    Returns:
        valid: Whether or not the verification code is valid
        reason: The reason why or why not the code is valid
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        code_object = VerificationCode.objects.filter(
            code=body["code"], user_uuid=body["user_uuid"]
        ).first()

        if code_object:
            if timezone.now() < code_object.expires:
                code_object.verified = True
                code_object.save()
                return JsonResponse({"valid": True, "reason": "valid"}, safe=False)

            else:
                return JsonResponse({"valid": False, "reason": "expired"}, safe=False)
        else:
            return JsonResponse(
                {"valid": False, "reason": "does_not_exist"}, safe=False, status=400
            )
    else:
        return HttpResponse("Request is not a POST request!", status=501)


def create_account(request):
    """
    Creates a new user account and signs the user in

    Body Parameters:
        uuid: The uuid of the user
        display-name: The provided display name of the user
        team-number: The team number of the user
        email: The email the user provided
        password: The password the user is setting
        verify: Weather or not to check if the account has verified
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        code_verified = VerificationCode.objects.filter(
            user_uuid=body["uuid"], verified=True
        ).first()

        if code_verified or not body["verify"]:
            try:
                if body["verify"]:
                    code_verified.delete()

                user = User.objects.create_user(
                    body["email"],
                    body["email"],
                    body["password"],
                )
                user.first_name = body["display_name"]
                user.save()

                profile = Profile(
                    user=user,
                    display_name=body["display_name"],
                    team_number=body["team_number"],
                )
                profile.save()

                email.send_welcome([body["email"]], body["display_name"])

                user = authenticate(
                    request,
                    username=body["email"],
                    password=body["password"],
                )

                if user is not None:
                    login(request, user)

                    return HttpResponse("success", status=200)
                else:
                    return HttpResponse("invalid login", status=401)

            except IntegrityError:
                return HttpResponse("username_exists", status=401)

            except Exception:
                return HttpResponse("error", status=500)
        else:
            return HttpResponse("invalid verification code", status=401)

    else:
        return HttpResponse("Request is not a POST request!", status=501)


def get_authentication_status(request):
    """
    Gets the authentication status of the session

    Returns:
        authenticated: Whether or not the user is authenticated
        username: The username of the user
        display_name: The display name of the user
        team_number: The team number of the user
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            return JsonResponse(
                {
                    "authenticated": True,
                    "username": request.user.username,
                    "display_name": request.user.profile.display_name,
                    "team_number": request.user.profile.team_number,
                },
                safe=False,
            )
        else:
            return JsonResponse(
                {
                    "authenticated": False,
                    "username": "",
                    "display_name": "",
                    "team_number": "",
                },
                safe=False,
            )
    else:
        return HttpResponse("Request is not a POST request!", status=501)


def save_profile(request):
    """
    Saves the profile of the user

    Body Parameters:
        user_id: The id of the user
        display_name: The display name of the user
        team_number: The team number of the user
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except KeyError:
            return HttpResponse(request, "No body found in request", status=400)

        user = User.objects.filter(id=body["user_id"]).first()

        profile = Profile.objects.filter(user=user).first()
        profile.display_name = body["display_name"]
        profile.team_number = body["team_number"]
        profile.save()

        return HttpResponse("success", status=200)
    else:
        return HttpResponse("Request is not a POST request!", status=501)
