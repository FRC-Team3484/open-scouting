from django.test import TestCase
from authentication.models import User, Profile


class GetAnalyticsTest(TestCase):
    def setUp(self):
        user = User.objects.create_user("test", "test", "test")
        user.is_superuser = True
        user.is_staff = True
        user.save()

        profile = Profile(user=user, display_name="test", team_number="1234")
        profile.save()

    def test_get_analytics(self):
        self.client.login(username="test", password="test")

        response = self.client.post("/analytics/get_analytics")
        self.assertEqual(response.status_code, 200)
