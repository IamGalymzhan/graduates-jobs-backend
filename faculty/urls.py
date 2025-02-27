from django.urls import path
from .views import FacultyStatisticsView, FacultyApplicationsView

urlpatterns = [
    path("stats/", FacultyStatisticsView.as_view(), name="faculty-stats"),
    path("applications/", FacultyApplicationsView.as_view(), name="faculty-applications"),
]
