from django.urls import path
from .views import ApplyForJobView, EmployerJobApplicationsView, JobPostListCreateView, JobPostDetailView

urlpatterns = [
    path("jobs/", JobPostListCreateView.as_view(), name="job-list-create"),
    path("jobs/<int:pk>/", JobPostDetailView.as_view(), name="job-detail"),
    path("jobs/<int:job_id>/apply/", ApplyForJobView.as_view(), name="apply-for-job"),
    path("employer/applications/", EmployerJobApplicationsView.as_view(), name="employer-applications"),

]
