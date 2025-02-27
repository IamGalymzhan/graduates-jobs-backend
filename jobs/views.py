from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters
from .models import JobApplication, JobPost
from .serializers import JobApplicationSerializer, JobPostSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from jobs import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied


class JobPostListCreateView(generics.ListCreateAPIView):
    queryset = JobPost.objects.all().order_by("-created_at")
    serializer_class = JobPostSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["job_type", "location"]  # ✅ Enables filtering by job type & location
    search_fields = ["title", "description", "location", "job_type", "requirements"]
    ordering_fields = ["created_at", "salary"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        """Ensure only employers can create jobs and assign employer automatically."""
        if self.request.user.user_type != "employer":
            raise serializers.ValidationError({"error": "Only employers can post jobs."}) 
        serializer.save(employer=self.request.user) 

class JobPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # ✅ Students, faculty, and admins can view all job posts
        if user.user_type in ["student", "faculty", "admin"]:
            return JobPost.objects.all()

        # ✅ Employers can only see their own job posts
        return JobPost.objects.filter(employer=user)

class ApplyForJobView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # ✅ Supports file uploads

    def perform_create(self, serializer):
        student = self.request.user
        job_id = self.kwargs["job_id"]
        job = get_object_or_404(JobPost, id=job_id)

        if student.user_type != "student":
            raise serializers.ValidationError({"error": "Only students can apply for jobs."})

        serializer.save(student=student, job=job)

class StudentJobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # ✅ Ensure only students can see their own applications
        if user.user_type != "student":
            raise PermissionDenied("Only students can view their job applications.")

        return JobApplication.objects.filter(student=user)

class EmployerJobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(job__employer=self.request.user)
