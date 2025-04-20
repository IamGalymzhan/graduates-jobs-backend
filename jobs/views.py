from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
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
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Only the employer who created the job post or an admin can delete it
        if request.user.user_type == "employer" and instance.employer != request.user:
            return Response(
                {"error": "You can only delete your own job posts"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Students and faculty cannot delete job posts
        if request.user.user_type in ["student"]:
            return Response(
                {"error": "Only employers can delete their own job posts or admins can delete any job post"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)

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

class JobApplicationsManagementView(generics.ListAPIView):
    """View for employers to see applications for their job posts and admins to see all applications."""
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Admin users can see all applications
        if user.user_type == "admin" or user.user_type == "faculty":
            return JobApplication.objects.all()
            
        # Employers can only see applications for their own job posts
        if user.user_type == "employer":
            return JobApplication.objects.filter(job__employer=user)
            
        # Other user types aren't allowed to access this endpoint
        raise PermissionDenied("Only employers can view applications for their job posts, or admins can view all applications.")

class JobApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Students can only view their own applications
        if user.user_type == "student":
            return JobApplication.objects.filter(student=user)
        
        # Employers can only view applications for their job posts
        elif user.user_type == "employer":
            return JobApplication.objects.filter(job__employer=user)
        
        # Admins can view all applications
        elif user.user_type == "admin" or user.user_type == "faculty":
            return JobApplication.objects.all()
        
        return JobApplication.objects.none()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Only employers should be able to add feedback
        if request.user.user_type != "employer" or instance.job.employer != request.user:
            return Response(
                {"error": "Only the employer who posted this job can provide feedback"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # If the request is only to update feedback, only update that field
        if len(request.data) == 1 and 'feedback' in request.data:
            instance.feedback = request.data['feedback']
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Only the student who created the application or an admin can delete it
        if request.user.user_type == "student" and instance.student != request.user:
            return Response(
                {"error": "You can only delete your own applications"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Employers cannot delete applications
        if request.user.user_type == "employer":
            return Response(
                {"error": "Employers cannot delete job applications"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
