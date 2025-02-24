from rest_framework import serializers
from .models import JobPost

class JobPostSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source="employer.full_name", read_only=True)  # ✅ Ensures employer name is fetched

    class Meta:
        model = JobPost
        fields = ["id", "employer", "employer_name", "title", "description", "requirements", "salary", "location", "job_type", "created_at"]
        read_only_fields = ["employer", "created_at"]
