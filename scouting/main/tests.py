from django.test import TestCase, Client
from django.conf import settings
from authentication.models import User, Profile
from main.models import Data, Event, PitGroup

import uuid
import json


class IndexPageTest(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user("test", "test", "test")
        user.save()

        profile = Profile(user=user, display_name="test", team_number="1234")
        profile.save()

    def test_index_anonymous(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class ContributePageTest(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user("test", "test", "test")
        user.save()

        profile = Profile(user=user, display_name="test", team_number="1234")
        profile.save()

    def test_contribute_anonymous(self):
        response = self.client.get("/contribute")
        self.assertEqual(response.status_code, 200)

    def test_contribute_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/contribute")
        self.assertEqual(response.status_code, 200)


class PitsPageTest(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user("test", "test", "test")
        user.save()

        profile = Profile(user=user, display_name="test", team_number="1234")
        profile.save()

    def test_pits_anonymous(self):
        response = self.client.get("/pits")
        self.assertEqual(response.status_code, 200)

    def test_pits_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/pits")
        self.assertEqual(response.status_code, 200)


class AdvancedDataPageTest(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create_user("test", "test", "test")
        user.save()

        profile = Profile(user=user, display_name="test", team_number="1234")
        profile.save()

    def test_advanced_data_anonymous(self):
        response = self.client.get("/advanced_data")
        self.assertEqual(response.status_code, 200)

    def test_advanced_data_authenticated(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/advanced_data")
        self.assertEqual(response.status_code, 200)


class ServiceWorkerPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_service_worker(self):
        response = self.client.get("/sw.js")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/javascript")


class SubmitTest(TestCase):
    def setUp(self):
        self.client = Client()

        session = self.client.session
        session["username"] = "test"
        session["team_number"] = "1234"
        session.save()

        self.uuid = uuid.uuid4().hex

        self.user = User.objects.create_user("test", "test", "test")
        self.user.save()

        profile = Profile(user=self.user, display_name="test", team_number="1234")
        profile.save()

    def test_submit_custom_anonymous(self):
        data = {
            "uuid": self.uuid,
            "data": "{}",
            "event_name": "test",
            "event_code": "test",
            "custom": "true",
            "year": 2024,
        }

        response = self.client.post("/submit", data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        data = Data.objects.first()
        self.assertEqual(data.event, "test")
        self.assertEqual(data.event_code, "test")
        self.assertEqual(data.year, 2024)
        self.assertEqual(data.data, {})
        self.assertEqual(data.event_model.custom, True)
        self.assertEqual(data.user_created, None)

    def test_submit_custom_authenticated(self):
        data = {
            "uuid": self.uuid,
            "data": "{}",
            "event_name": "test",
            "event_code": "test",
            "custom": "true",
            "year": 2024,
        }

        self.client.login(username="test", password="test")

        response = self.client.post("/submit", data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        data = Data.objects.first()
        self.assertEqual(data.event, "test")
        self.assertEqual(data.event_code, "test")
        self.assertEqual(data.year, 2024)
        self.assertEqual(data.data, {})
        self.assertEqual(data.event_model.custom, True)
        self.assertEqual(data.user_created, self.user)

    def test_submit_normal_anonymous(self):
        data = {
            "uuid": self.uuid,
            "data": "{}",
            "event_name": "test",
            "event_code": "test",
            "custom": "false",
            "year": 2024,
        }

        response = self.client.post("/submit", data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        data = Data.objects.first()
        self.assertEqual(data.event, "test")
        self.assertEqual(data.event_code, "test")
        self.assertEqual(data.year, 2024)
        self.assertEqual(data.data, {})
        self.assertEqual(data.event_model.custom, False)
        self.assertEqual(data.user_created, None)

    def test_submit_normal_authenticated(self):
        data = {
            "uuid": self.uuid,
            "data": "{}",
            "event_name": "test",
            "event_code": "test",
            "custom": "false",
            "year": 2024,
        }

        self.client.login(username="test", password="test")

        response = self.client.post("/submit", data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        data = Data.objects.first()
        self.assertEqual(data.event, "test")
        self.assertEqual(data.event_code, "test")
        self.assertEqual(data.year, 2024)
        self.assertEqual(data.data, {})
        self.assertEqual(data.event_model.custom, False)
        self.assertEqual(data.user_created, self.user)


class GetCustomEventsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_custom_events(self):
        data = {"year": 2024}

        response = self.client.post(
            "/get_custom_events", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response["Content-Type"], "application/json")


class CreateCustomEventTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user("test", "test", "test")
        self.user.save()

        profile = Profile(user=self.user, display_name="test", team_number="1234")
        profile.save()

    def test_create_custom_event_anonymous(self):
        data = {
            "name": "test",
            "year": 2024,
            "date_begins": "2024-01-01",
            "date_ends": "2024-01-01",
            "location": "test",
            "type": "test",
        }

        response = self.client.post(
            "/create_custom_event", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        event = Event.objects.first()
        self.assertEqual(event.year, 2024)
        self.assertEqual(event.name, "test")
        self.assertEqual(event.custom, True)

        self.assertEqual(event.custom_data["name"], "test")
        self.assertEqual(event.custom_data["year"], 2024)
        self.assertEqual(event.custom_data["date_begins"], "2024-01-01")
        self.assertEqual(event.custom_data["date_ends"], "2024-01-01")
        self.assertEqual(event.custom_data["location"], "test")
        self.assertEqual(event.custom_data["type"], "test")

    def test_create_custom_event_authenticated(self):
        data = {
            "name": "test",
            "year": 2024,
            "date_begins": "2024-01-01",
            "date_ends": "2024-01-01",
            "location": "test",
            "type": "test",
        }

        self.client.login(username="test", password="test")

        response = self.client.post(
            "/create_custom_event", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        event = Event.objects.first()
        self.assertEqual(event.year, 2024)
        self.assertEqual(event.name, "test")
        self.assertEqual(event.custom, True)
        self.assertEqual(event.user_created, self.user)

        self.assertEqual(event.custom_data["name"], "test")
        self.assertEqual(event.custom_data["year"], 2024)
        self.assertEqual(event.custom_data["date_begins"], "2024-01-01")
        self.assertEqual(event.custom_data["date_ends"], "2024-01-01")
        self.assertEqual(event.custom_data["location"], "test")
        self.assertEqual(event.custom_data["type"], "test")


class GetYearDataTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_year_data(self):
        data = {"year": 2024}

        response = self.client.post(
            "/get_year_data", data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response["Content-Type"], "application/json")


class CheckLocalBackupReportsTest(TestCase):
    def setUp(self):
        self.client = Client()

        session = self.client.session
        session["username"] = "test"
        session["team_number"] = "1234"
        session.save()

        self.user = User.objects.create_user("test", "test", "test")
        self.user.save()

        self.uuid = uuid.uuid4().hex

        profile = Profile(user=self.user, display_name="test", team_number="1234")
        profile.save()

    def test_check_local_backup_reports_custom_anonymous(self):
        data = {
            "data": json.dumps(
                [
                    {
                        "uuid": self.uuid,
                        "event_name": "test",
                        "event_code": "test",
                        "year": 2024,
                        "custom": True,
                        "data": {},
                    }
                ]
            ),
        }

        response = self.client.post(
            "/check_local_backup_reports", data, content_type="application/json"
        )

        data = json.loads(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(data["reports_not_found"], 1)
        self.assertEqual(data["reports_found"], 0)

    def test_check_local_backup_reports_custom_authenticated(self):
        data = {
            "data": json.dumps(
                [
                    {
                        "uuid": self.uuid,
                        "event_name": "test",
                        "event_code": "test",
                        "year": 2024,
                        "custom": True,
                        "data": {},
                    }
                ]
            ),
        }

        self.client.login(username="test", password="test")
        response = self.client.post(
            "/check_local_backup_reports", data, content_type="application/json"
        )

        data = json.loads(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(data["reports_not_found"], 1)
        self.assertEqual(data["reports_found"], 0)

    def test_check_local_backup_reports_normal_anonymous(self):
        data = {
            "data": json.dumps(
                [
                    {
                        "uuid": self.uuid,
                        "event_name": "test",
                        "event_code": "test",
                        "year": 2024,
                        "custom": False,
                        "data": {},
                    }
                ]
            ),
        }

        response = self.client.post(
            "/check_local_backup_reports", data, content_type="application/json"
        )

        data = json.loads(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(data["reports_not_found"], 1)
        self.assertEqual(data["reports_found"], 0)

    def test_check_local_backup_reports_normal_authenticated(self):
        data = {
            "data": json.dumps(
                [
                    {
                        "uuid": self.uuid,
                        "event_name": "test",
                        "event_code": "test",
                        "year": 2024,
                        "custom": False,
                        "data": {},
                    }
                ]
            ),
        }

        self.client.login(username="test", password="test")
        response = self.client.post(
            "/check_local_backup_reports", data, content_type="application/json"
        )

        data = json.loads(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(data["reports_not_found"], 1)
        self.assertEqual(data["reports_found"], 0)


class UploadOfflineReports(TestCase):
    def setUp(self):
        self.client = Client()

        session = self.client.session
        session["username"] = "test"
        session["team_number"] = "1234"
        session.save()

        self.user = User.objects.create_user("test", "test", "test")
        self.user.save()

        self.uuid = uuid.uuid4().hex

        profile = Profile(user=self.user, display_name="test", team_number="1234")
        profile.save()

    def test_upload_offline_reports_custom_anonymous(self):
        data = {
            "data": json.dumps(
                [
                    {
                        "uuid": self.uuid,
                        "event_name": "test",
                        "event_code": "test",
                        "year": 2024,
                        "custom": True,
                        "data": {},
                    }
                ]
            ),
        }

        response = self.client.post(
            "/upload_offline_reports", data, content_type="application/json"
        )

        data = json.loads(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(data["reports_not_found"], 1)
        self.assertEqual(data["reports_found"], 0)

    def test_upload_offline_reports_custom_authenticated(self):
        data = {
            "data": json.dumps(
                [
                    {
                        "uuid": self.uuid,
                        "event_name": "test",
                        "event_code": "test",
                        "year": 2024,
                        "custom": True,
                        "data": {},
                    }
                ]
            ),
        }

        self.client.login(username="test", password="test")
        response = self.client.post(
            "/upload_offline_reports", data, content_type="application/json"
        )

        data = json.loads(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(data["reports_not_found"], 1)
        self.assertEqual(data["reports_found"], 0)

    def test_upload_offline_reports_normal_anonymous(self):
        data = {
            "data": json.dumps(
                [
                    {
                        "uuid": self.uuid,
                        "event_name": "test",
                        "event_code": "test",
                        "year": 2024,
                        "custom": False,
                        "data": {},
                    }
                ]
            ),
        }

        response = self.client.post(
            "/upload_offline_reports", data, content_type="application/json"
        )

        data = json.loads(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(data["reports_not_found"], 1)
        self.assertEqual(data["reports_found"], 0)

    def test_upload_offline_reports_normal_authenticated(self):
        data = {
            "data": json.dumps(
                [
                    {
                        "uuid": self.uuid,
                        "event_name": "test",
                        "event_code": "test",
                        "year": 2024,
                        "custom": False,
                        "data": {},
                    }
                ]
            ),
        }

        self.client.login(username="test", password="test")
        response = self.client.post(
            "/upload_offline_reports", data, content_type="application/json"
        )

        data = json.loads(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(data["reports_not_found"], 1)
        self.assertEqual(data["reports_found"], 0)


class GetPits(TestCase):
    def setUp(self):
        self.client = Client()

        event = Event(year=2024, name="test", event_code="test")
        event.save()

        pit_group = PitGroup(event=event, events_generated=True)
        pit_group.save()

    def test_get_pits_pit_group_does_not_exist(self):
        data = {
            "event_name": "test_not_real",
            "event_code": "test_not_real",
            "year": 2024,
            "custom": False,
        }

        response = self.client.post("/get_pits", data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_get_pits_pit_group_exists(self):
        data = {
            "event_name": "test",
            "event_code": "test",
            "year": 2024,
            "custom": False,
        }

        response = self.client.post("/get_pits", data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")


class UpdatePit(TestCase):
    def setUp(self):
        self.client = Client()

        event = Event(year=2024, name="test", event_code="test")
        event.save()

        pit_group = PitGroup(event=event, events_generated=True)
        pit_group.save()

    def test_update_pit(self):
        data = {
            "event_name": "test",
            "event_code": "test",
            "year": 2024,
            "custom": False,
            "data": json.dumps([]),
        }

        response = self.client.post(
            "/update_pit", data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)


class GetPitQuestions(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_pit_questions(self):
        data = {"year": 2024}

        response = self.client.post(
            "/get_pit_questions", data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")


class GetTeamsWithFilters(TestCase):
    def setUp(self):
        self.client = Client()

        event = Event(year=2024, name="test", event_code="test")
        event.save()

        data = Data(year=2024, event="test", event_code="test")
        data.save()
        data = Data(year=2024, event="test something", event_code="test something")
        data.save()

    def test_get_teams_with_filters(self):
        data = json.dumps({"year": 2024, "events": json.dumps([])})

        response = self.client.post(
            "/get_teams_with_filters", data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 0)


class GetEventsWithFilters(TestCase):
    def setUp(self):
        self.client = Client()

        event = Event(year=2024, name="test", event_code="test")
        event.save()

        data = Data(year=2024, event="test", event_code="test")
        data.data = [
            {
                "name": "team_number",
                "type": "large_integer",
                "value": "1234",
                "stat_type": "ignore",
                "game_piece": "",
            }
        ]
        data.save()
        data = Data(year=2024, event="test something", event_code="test something")
        data.data = [
            {
                "name": "team_number",
                "type": "large_integer",
                "value": "0000",
                "stat_type": "ignore",
                "game_piece": "",
            }
        ]
        data.save()

    def test_get_events_with_filters(self):
        data = json.dumps({"year": 2024, "teams": json.dumps([])})

        response = self.client.post(
            "/get_events_with_filters", data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 0)


class GetDataFromQuery(TestCase):
    def setUp(self):
        self.client = Client()

        event = Event(year=2024, name="test", event_code="test")
        event.save()

        data = Data(year=2024, event="test", event_code="test")
        data.data = [
            {
                "name": "team_number",
                "type": "large_integer",
                "value": "1234",
                "stat_type": "ignore",
                "game_piece": "",
            }
        ]
        data.save()

    def test_get_data_from_query(self):
        data = {"query": "?year=2024"}

        response = self.client.post(
            "/get_data_from_query", data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)

    def test_get_data_from_query_filtered(self):
        data = {"query": "?year=2024&teams=1234"}

        response = self.client.post(
            "/get_data_from_query", data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)


class GetVersion(TestCase):
    def test_get_version(self):
        response = self.client.post("/get_version")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        response_json = json.loads(response.content)
        self.assertEqual(response_json["version"], settings.SERVER_VERSION)
