from django.db import models
from users.models import CustomUser, UserType

class JobPost(models.Model):
    employer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="job_posts", limit_choices_to={"user_type": UserType.EMPLOYER}
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255)
    job_type = models.CharField(
        max_length=50,
        choices=[("full-time", "Full-Time"), ("part-time", "Part-Time"), ("internship", "Internship")],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
