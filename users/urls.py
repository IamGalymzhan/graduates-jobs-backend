from django.urls import path
from .views import RegisterView, LoginView, StudentProfileView, SkillListCreateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", StudentProfileView.as_view(), name="student-profile"),
    path("skills/", SkillListCreateView.as_view(), name="skill-list-create"),
]
