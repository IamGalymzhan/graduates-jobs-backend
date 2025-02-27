from django.urls import path
from .views import RegisterView, LoginView, StudentListView, StudentProfileView, SkillListCreateView, StudentPublicProfileView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", StudentProfileView.as_view(), name="student-profile"),
    path("skills/", SkillListCreateView.as_view(), name="skill-list-create"),
    path("profile/<int:pk>/", StudentPublicProfileView.as_view(), name="student-public-profile"),
    path("students/", StudentListView.as_view(), name="student-list"),
    
]
