from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserType(models.TextChoices):  
    STUDENT = "student", "Student"
    EMPLOYER = "employer", "Employer"
    ADMIN = "admin", "Admin"
    FACULTY = "faculty", "Faculty"

class Status(models.TextChoices):
    SEARCHING = "searching", "Searching for Job"
    WORKING = "working", "Currently Working"
    INTERNSHIP = "internship", "Internship"

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # ✅ Removed username
    email = models.EmailField(unique=True)  # ✅ Use email as unique identifier
    full_name = models.CharField(max_length=255, default="")
    user_type = models.CharField(
        max_length=20, choices=UserType.choices, default=UserType.STUDENT
    )
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    # Student-specific fields
    education = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SEARCHING
    )
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    # Employer-specific fields
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)

    objects = CustomUserManager()  # ✅ Use custom manager

    USERNAME_FIELD = "email"  # ✅ Use email instead of username
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.full_name
