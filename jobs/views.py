from rest_framework import generics, permissions
from .models import JobPost
from .serializers import JobPostSerializer

class JobPostListCreateView(generics.ListCreateAPIView):
    queryset = JobPost.objects.all().order_by("-created_at")
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)  # ✅ Assign the logged-in employer


class JobPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user)  # Employers manage only their jobs
