from django.contrib import admin
from .models import JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'posted_by', 'employment_type', 'status', 'created_at']
    list_filter = ['status', 'employment_type', 'experience_level']
    search_fields = ['title', 'company', 'skills_required', 'posted_by__email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'referrals_count']
    ordering = ['-created_at']

    actions = ['make_active', 'make_closed', 'remove_posts']

    def make_active(self, request, queryset):
        queryset.update(status='active')
    make_active.short_description = "Mark selected jobs as Active"

    def make_closed(self, request, queryset):
        queryset.update(status='closed')
    make_closed.short_description = "Close selected job postings"

    def remove_posts(self, request, queryset):
        queryset.update(status='removed')
    remove_posts.short_description = "Remove selected posts (Admin action)"
