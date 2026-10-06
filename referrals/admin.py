from django.contrib import admin
from .models import ReferralRequest


@admin.register(ReferralRequest)
class ReferralRequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'job', 'alumni', 'status', 'admin_outcome', 'created_at']
    list_filter = ['status', 'admin_outcome']
    search_fields = ['requester__email', 'alumni__email', 'job__title']
    list_editable = ['admin_outcome']
    readonly_fields = ['created_at', 'updated_at', 'responded_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Request Details', {
            'fields': ('job', 'requester', 'alumni', 'cover_note')
        }),
        ('Alumni Response', {
            'fields': ('status', 'alumni_note', 'responded_at')
        }),
        ('Admin Review', {
            'fields': ('admin_outcome', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
