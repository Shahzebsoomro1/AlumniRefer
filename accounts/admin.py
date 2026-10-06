from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = (
        'bio', 'company', 'job_title', 'years_of_experience',
        'linkedin_url', 'skills', 'location', 'phone',
        'is_verified', 'is_accepting_referrals', 'avatar'
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Status', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'job_title', 'is_verified', 'is_accepting_referrals']
    list_filter = ['is_verified', 'is_accepting_referrals']
    search_fields = ['user__email', 'user__first_name', 'company', 'skills']
    list_editable = ['is_verified']
