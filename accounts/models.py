from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('alumni', 'Alumni'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_job_seeker(self):
        return self.role == 'job_seeker'

    @property
    def is_alumni(self):
        return self.role == 'alumni'

    @property
    def is_portal_admin(self):
        return self.role in ['admin', 'super_admin']

    @property
    def is_super_admin(self):
        return self.role == 'super_admin'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    company = models.CharField(max_length=200, blank=True, help_text="Current company (for alumni)")
    job_title = models.CharField(max_length=200, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    linkedin_url = models.URLField(blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    location = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    is_accepting_referrals = models.BooleanField(
        default=True,
        help_text="Alumni: are you open to referral requests?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"

    def get_skills_list(self):
        if self.skills:
            return [s.strip() for s in self.skills.split(',') if s.strip()]
        return []

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/img/default-avatar.svg'
