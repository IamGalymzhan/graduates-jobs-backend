from rest_framework import generics, permissions, filters
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer, StudentProfileSerializer, SkillSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser, Skill
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        return {"request": self.request}

    def update(self, request, *args, **kwargs):
        print("Received skills data:", request.data.getlist("skills"))
        return super().update(request, *args, **kwargs)

class StudentListView(generics.ListAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.user_type in ["employer", "faculty", "admin"]:
            return CustomUser.objects.filter(user_type="student")

        raise PermissionDenied("You do not have permission to view this list.")


class StudentPublicProfileView(generics.RetrieveAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(user_type="student")

    def get_object(self):
        student_id = self.kwargs.get("pk")
        user = self.request.user

        if user.user_type == "admin":
            return get_object_or_404(CustomUser, id=student_id, user_type="student")

        if user.user_type == "student" and user.id != int(student_id):
            raise PermissionDenied("You are not allowed to view this profile.")

        if user.user_type in ["employer", "faculty", "admin"]:
            return get_object_or_404(CustomUser, id=student_id, user_type="student")

        raise PermissionDenied("You do not have permission to access this profile.")


class SkillPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = "page_size"
    max_page_size = 50

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all().order_by("name")
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SkillPagination
    filter_backends = [filters.SearchFilter] 
    search_fields = ["name"]
