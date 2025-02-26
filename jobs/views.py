from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters
from .models import JobApplication, JobPost
from .serializers import JobApplicationSerializer, JobPostSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from jobs import serializers
from django_filters.rest_framework import DjangoFilterBackend


class JobPostListCreateView(generics.ListCreateAPIView):
    queryset = JobPost.objects.all().order_by("-created_at")
    serializer_class = JobPostSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["job_type", "location"]  # ✅ Enables filtering by job type & location
    search_fields = ["title", "description", "location", "job_type", "requirements"]
    ordering_fields = ["created_at", "salary"]
    ordering = ["-created_at"]

class JobPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user)  # Employers manage only their jobs

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

class EmployerJobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(job__employer=self.request.user)
