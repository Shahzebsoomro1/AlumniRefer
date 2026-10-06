from django.db import models
from django.conf import settings
from django.urls import reverse


class JobPosting(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level (0-2 yrs)'),
        ('mid', 'Mid Level (2-5 yrs)'),
        ('senior', 'Senior Level (5+ yrs)'),
        ('lead', 'Lead / Manager'),
        ('executive', 'Executive'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('removed', 'Removed by Admin'),
    ]

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_postings',
        limit_choices_to={'role': 'alumni'}
    )
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default='mid')
    description = models.TextField()
    requirements = models.TextField(help_text="List key requirements")
    skills_required = models.CharField(max_length=500, blank=True, help_text="Comma-separated skills")
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g. $80k–$120k")
    application_deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    referrals_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'

    def __str__(self):
        return f"{self.title} at {self.company}"

    def get_absolute_url(self):
        return reverse('jobs:detail', kwargs={'pk': self.pk})

    def get_skills_list(self):
        if self.skills_required:
            return [s.strip() for s in self.skills_required.split(',') if s.strip()]
        return []

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def pending_referrals(self):
        return self.referral_requests.filter(status='pending').count()
