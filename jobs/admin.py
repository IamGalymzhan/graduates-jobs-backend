from django.contrib import admin
from .models import JobPost, JobApplication

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'job_type', 'location', 'salary', 'created_at')
    list_filter = ('job_type', 'created_at', 'location')
    search_fields = ('title', 'description', 'employer__full_name', 'employer__company_name', 'location')
    filter_horizontal = ('skills',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'description', 'requirements', 'skills')
        }),
        ('Job Details', {
            'fields': ('job_type', 'salary', 'location')
        }),
        ('Employer', {
            'fields': ('employer',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employer')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'applied_at', 'has_resume', 'has_feedback')
    list_filter = ('applied_at', 'job__job_type', 'job__location')
    search_fields = ('student__full_name', 'student__email', 'job__title', 'job__employer__company_name')
    date_hierarchy = 'applied_at'
    ordering = ('-applied_at',)
    readonly_fields = ('applied_at',)
    
    fieldsets = (
        ('Application Info', {
            'fields': ('student', 'job', 'applied_at')
        }),
        ('Application Content', {
            'fields': ('cover_letter', 'resume')
        }),
        ('Employer Feedback', {
            'fields': ('feedback',),
            'classes': ('collapse',),
        }),
    )
    
    def has_resume(self, obj):
        return bool(obj.resume)
    has_resume.boolean = True
    has_resume.short_description = 'Resume Uploaded'
    
    def has_feedback(self, obj):
        return bool(obj.feedback)
    has_feedback.boolean = True
    has_feedback.short_description = 'Has Feedback'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'job', 'job__employer')
