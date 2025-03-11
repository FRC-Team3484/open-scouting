from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contribute", views.contribute, name="contribute"),
    path("data", views.data, name="data"),
    path("pits", views.pits, name="pits"),
    path("advanced_data", views.advanced_data, name="advanced_data"),
    path("sw.js", views.service_worker),
    path("submit", views.submit, name="submit"),
    path("get_data", views.get_data, name="get_data"),
    path("get_custom_events", views.get_custom_events, name="get_custom_events"),
    path("create_custom_event", views.create_custom_event, name="create_custom_event"),
    path("get_year_data", views.get_year_data, name="get_year_data"),
    path(
        "check_local_backup_reports",
        views.check_local_backup_reports,
        name="check_local_backup_reports",
    ),
    path(
        "upload_offline_reports",
        views.upload_offline_reports,
        name="upload_offline_reports",
    ),
    path("get_pits", views.get_pits, name="get_pits"),
    path("update_pits", views.update_pits, name="update_pits"),
    path("get_pit_questions", views.get_pit_questions, name="get_pit_questions"),
    path(
        "get_teams_with_filters",
        views.get_teams_with_filters,
        name="get_teams_with_filters",
    ),
    path(
        "get_events_with_filters",
        views.get_events_with_filters,
        name="get_events_with_filters",
    ),
    path("get_data_from_query", views.get_data_from_query, name="get_data_from_query"),
]
