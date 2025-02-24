from rest_framework import generics, permissions, filters
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer, StudentProfileSerializer, SkillSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser, Skill
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # ✅ Allows file uploads

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        return {"request": self.request}

    def update(self, request, *args, **kwargs):
        print("Received skills data:", request.data.getlist("skills"))  # ✅ Debugging skills input
        return super().update(request, *args, **kwargs)

class SkillPagination(PageNumberPagination):
    page_size = 10  # ✅ Default: 10 skills per page
    page_size_query_param = "page_size"
    max_page_size = 50

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all().order_by("name")
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SkillPagination
    filter_backends = [filters.SearchFilter] 
    search_fields = ["name"]  