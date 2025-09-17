from django.urls import path
from . import views

urlpatterns = [
    path("status", views.StatusView.as_view()),
    path("event/<int:year>", views.EventListView.as_view()),
    path("event/<int:year>/<str:event_code>", views.EventDetailView.as_view()),
    path("event/<int:year>/<str:event_code>/data", views.EventDataView.as_view()),
    path("event/<int:year>/<str:event_code>/pit", views.EventPitView.as_view()),
    path("data/<int:year>", views.DataYearView.as_view()),
    path("data/<int:year>/<int:team_number>", views.DataTeamView.as_view()),
    path("pit/<int:year>", views.PitYearView.as_view()),
    path("pit/<int:year>/<int:team_number>", views.PitTeamView.as_view()),
    path("team/<int:year>", views.TeamYearView.as_view()),
    path("team/<int:year>/<int:team_number>", views.TeamDetailView.as_view()),
    path("team/<int:year>/<int:team_number>/data", views.TeamDataView.as_view()),
    path("team/<int:year>/<int:team_number>/pit", views.TeamPitView.as_view()),
]
