from django.urls import path
from .views import JobPostListCreateView, JobPostDetailView

urlpatterns = [
    path("jobs/", JobPostListCreateView.as_view(), name="job-list-create"),
    path("jobs/<int:pk>/", JobPostDetailView.as_view(), name="job-detail"),
]
