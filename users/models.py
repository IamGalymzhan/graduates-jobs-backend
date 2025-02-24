from django.contrib.auth.models import AbstractUser
from django.db import models

class UserType(models.TextChoices):  
    STUDENT = "student", "Student"
    EMPLOYER = "employer", "Employer"
    ADMIN = "admin", "Admin"

class Status(models.TextChoices):
    SEARCHING = "searching", "Searching for Job"
    WORKING = "working", "Currently Working"
    INTERNSHIP = "internship", "Internship"

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, default="")
    email = models.EmailField(unique=True)
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

    def __str__(self):
        return self.full_name
