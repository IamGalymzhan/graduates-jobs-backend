from rest_framework import serializers
from .models import JobPost, JobApplication

class JobPostSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source="employer.full_name", read_only=True)  # ✅ Ensures employer name is fetched

    class Meta:
        model = JobPost
        fields = ["id", "employer", "employer_name", "title", "description", "requirements", "salary", "location", "job_type", "created_at"]
        read_only_fields = ["employer", "created_at"]

class JobApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source="student.full_name")
    job_title = serializers.ReadOnlyField(source="job.title")

    class Meta:
        model = JobApplication
        fields = ["id", "student", "student_name", "job", "job_title", "cover_letter", "resume", "applied_at"]
        read_only_fields = ["student", "job", "applied_at"]
