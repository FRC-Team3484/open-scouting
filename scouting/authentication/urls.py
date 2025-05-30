from django.urls import path

from . import views

urlpatterns = [
    path("", views.auth, name="auth"),
    path("profile", views.profile, name="profile"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("sign_out", views.sign_out, name="sign_out"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path("change_password", views.change_password, name="change_password"),
    path(
        "send_verification_code",
        views.send_verification_code,
        name="send_verification_code",
    ),
    path(
        "check_verification_code",
        views.check_verification_code,
        name="check_verification_code",
    ),
    path("create_account", views.create_account, name="create_account"),
    path(
        "get_authentication_status",
        views.get_authentication_status,
        name="get_authentication_status",
    ),
    path("save_profile", views.save_profile, name="save_profile"),
]
