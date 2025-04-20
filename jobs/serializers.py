from rest_framework import serializers
from .models import JobPost, JobApplication

class JobPostSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source="employer.full_name", read_only=True)

    class Meta:
        model = JobPost
        fields = ["id", "title", "description", "requirements", "salary", "location", "job_type", "created_at", "employer_name", "skills"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["skills"] = [{"id": skill.id, "name": skill.name} for skill in instance.skills.all()]

        return data

class JobApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source="student.full_name")
    job_title = serializers.ReadOnlyField(source="job.title")
    job_location = serializers.ReadOnlyField(source="job.location")  # ✅ Add more job details
    job_employer = serializers.ReadOnlyField(source="job.employer.full_name")

    class Meta:
        model = JobApplication
        fields = ["id", "student_name", "job_title", "job_location", "job_employer", "cover_letter", "resume", "applied_at", "feedback"]
        read_only_fields = ["student_name", "job_title", "job_location", "job_employer", "applied_at"]