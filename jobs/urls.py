from django.urls import path
from .views import (
    ApplyForJobView,
    JobApplicationsManagementView,
    JobPostListCreateView,
    JobPostDetailView,
    StudentJobApplicationsView,
    JobApplicationDetailView
)

urlpatterns = [
    path("jobs/", JobPostListCreateView.as_view(), name="job-list-create"),
    path("jobs/<int:pk>/", JobPostDetailView.as_view(), name="job-detail"),
    path("jobs/<int:job_id>/apply/", ApplyForJobView.as_view(), name="apply-for-job"),
    path("manage/applications/", JobApplicationsManagementView.as_view(), name="manage-applications"),
    path("applications/", StudentJobApplicationsView.as_view(), name="student-applications"),
    path("applications/<int:pk>/", JobApplicationDetailView.as_view(), name="application-detail"),
]
