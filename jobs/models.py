from django.db import models
from users.models import CustomUser, Skill, UserType

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
    skills = models.ManyToManyField(Skill, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"user_type": UserType.STUDENT})
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField()
    resume = models.FileField(upload_to="job_applications/", blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True, help_text="Feedback from the employer about this application")

    def __str__(self):
        return f"{self.student.full_name} applied for {self.job.title}"
