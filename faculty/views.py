from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from jobs import serializers
from users.models import CustomUser
from jobs.models import JobPost, JobApplication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class FacultyStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != "faculty":
            return Response({"error": "Unauthorized"}, status=403)

        last_6_months = now() - timedelta(days=180)

        # ✅ User growth over time
        student_growth = (
            CustomUser.objects.filter(user_type="student", date_joined__gte=last_6_months)
            .annotate(month=TruncMonth("date_joined"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )
        student_growth = [{"month": entry["month"].strftime("%Y-%m"), "count": entry["count"]} for entry in student_growth]

        # ✅ Most needed skills
        most_needed_skills = (
            JobPost.objects.values("skills__name")
            .exclude(skills__name__isnull=True)
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        # ✅ Student status distribution
        student_statuses = (
            CustomUser.objects.filter(user_type="student")
            .values("status")
            .annotate(count=Count("id"))
        )

        return Response({
            "total_students": CustomUser.objects.filter(user_type="student").count(),
            "total_employers": CustomUser.objects.filter(user_type="employer").count(),
            "total_jobs": JobPost.objects.count(),
            "total_applications": JobApplication.objects.count(),
            "student_growth": student_growth,
            "most_needed_skills": list(most_needed_skills),
            "student_statuses": list(student_statuses),
        })

class FacultyApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != "faculty":
            return Response({"error": "Unauthorized"}, status=403)

        applications = JobApplication.objects.all()
        serializer = serializers.JobApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    