from django.test import TestCase, Client
from authentication.models import User, Profile, VerificationCode, Settings
from django.utils import timezone

import uuid
import json


class AuthenticationPageTest(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user("test", "test", "test")
        user.save()

        profile = Profile(user=user, display_name="test", team_number="1234")
        profile.save()

    def test_authentication_anonymous(self):
        response = self.client.get("/authentication/")
        self.assertEqual(response.status_code, 200)

    def test_authentication_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/authentication/")
        self.assertEqual(response.status_code, 200)


class SignInTest(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user("test", "test", "test")
        user.save()

        profile = Profile(user=user, display_name="test", team_number="1234")
        profile.save()

    def test_sign_in(self):
        data = {
            "email": "test",
            "password": "test",
        }

        response = self.client.post(
            "/authentication/sign_in", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get("_auth_user_id"))


class SignOutTest(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user("test", "test", "test")
        user.save()

        profile = Profile(user=user, display_name="test", team_number="1234")
        profile.save()

    def test_sign_out(self):
        self.client.login(username="test", password="test")
        response = self.client.post("/authentication/sign_out")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.session.get("_auth_user_id"))


# TODO: Implement this test when the corresponding feature is implemented
# class ForgotPasswordTest(TestCase):
#     def setUp(self):
#         self.client = Client()

#         user = User.objects.create_user("test", "test", "test")
#         user.save()

#         profile = Profile(user=user, display_name="test", team_number="1234")
#         profile.save()

#     def test_forgot_password_anonymous(self):
#         pass

#     def test_forgot_password_authenticated(self):
#         pass


# TODO: Implement this test when the corresponding feature is implemented
# class ChangePasswordTest(TestCase):
#     def setUp(self):
#         self.client = Client()

#         user = User.objects.create_user("test", "test", "test")
#         user.save()

#         profile = Profile(user=user, display_name="test", team_number="1234")
#         profile.save()

#     def test_change_password_anonymous(self):
#         pass

#     def test_change_password_authenticated(self):
#         pass


class SendVerificationCodeTest(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user("test", "test", "test")
        user.save()

        self.uuid = uuid.uuid4().hex

        profile = Profile(user=user, display_name="test", team_number="1234")
        profile.save()

    def test_send_verification_code(self):
        data = {
            "email": "test",
            "display_name": "test",
            "uuid": self.uuid,
        }

        response = self.client.post(
            "/authentication/send_verification_code",
            data,
            content_type="application/json",
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["user_uuid"], self.uuid)

        verification_code = VerificationCode.objects.first()
        self.assertEqual(str(verification_code.user_uuid).replace("-", ""), self.uuid)


class CheckVerificationCodeTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.uuid = uuid.uuid4().hex

        user = User.objects.create_user("test", "test", "test")
        user.save()

        profile = Profile(user=user, display_name="test", team_number="1234")
        profile.save()

        verification_code = VerificationCode.objects.create(
            code="123456",
            user_uuid=self.uuid,
            verified=True,
            created=timezone.now(),
            expires=timezone.now() + timezone.timedelta(minutes=10),
        )
        verification_code.save()

    def test_check_verification_code(self):
        data = {
            "code": "123456",
            "user_uuid": self.uuid,
        }

        response = self.client.post(
            "/authentication/check_verification_code",
            data,
            content_type="application/json",
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["valid"], True)


class CreateAccountTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.uuid = uuid.uuid4().hex

        verification_code = VerificationCode(
            code="123456",
            user_uuid=self.uuid,
            verified=True,
            created=timezone.now(),
            expires=timezone.now() + timezone.timedelta(minutes=10),
        )
        verification_code.save()

    def test_create_account(self):
        data = {
            "email": "test",
            "password": "test",
            "display_name": "test",
            "team_number": "test",
            "uuid": self.uuid,
            "verify": True,
        }

        response = self.client.post(
            "/authentication/create_account", data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        user = User.objects.first()
        self.assertEqual(user.email, "test")
        self.assertEqual(user.username, "test")

        profile = Profile.objects.first()
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.display_name, "test")
        self.assertEqual(profile.team_number, "test")


class GetAuthenticationStatusTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user("test", "test", "test")
        self.user.save()

        profile = Profile(user=self.user, display_name="test", team_number="1234")
        profile.save()

    def test_get_authentication_status_anonymous(self):
        response = self.client.post("/authentication/get_authentication_status")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json()["authenticated"], False)

    def test_get_authentication_status_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.post("/authentication/get_authentication_status")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json()["authenticated"], True)


class SaveProfileTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user("test", "test", "test")
        self.user.save()

        profile = Profile(user=self.user, display_name="test", team_number="1234")
        profile.save()

    def test_save_profile(self):
        data = {
            "user_id": self.user.id,
            "display_name": "test",
            "team_number": "1234",
        }

        response = self.client.post(
            "/authentication/save_profile", data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)


class GetUserSettingsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user("test", "test", "test")
        self.user.save()

        profile = Profile(user=self.user, display_name="test", team_number="1234")
        profile.save()

        settings = Settings(user=self.user)
        settings.save()

    def test_get_user_settings(self):
        self.client.login(username="test", password="test")

        response = self.client.post("/authentication/get_user_settings")

        self.assertEqual(response.status_code, 200)


class SetUserSettingsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user("test", "test", "test")
        self.user.save()

        profile = Profile(user=self.user, display_name="test", team_number="1234")
        profile.save()

        settings = Settings(user=self.user)
        settings.save()

    def test_set_user_settings(self):
        self.client.login(username="test", password="test")

        data = [{"key": "favorite_events", "value": "test"}]

        response = self.client.post(
            "/authentication/set_user_settings", data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
