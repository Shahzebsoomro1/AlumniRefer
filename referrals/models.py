from django.db import models
from django.conf import settings
from jobs.models import JobPosting


class ReferralRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    ADMIN_OUTCOME_CHOICES = [
        ('', 'Not Yet Reviewed'),
        ('hired', 'Hired'),
        ('interviewed', 'Interviewed'),
        ('not_hired', 'Not Hired'),
        ('dropped', 'Candidate Dropped Out'),
    ]

    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name='referral_requests'
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referral_requests_sent',
        limit_choices_to={'role': 'job_seeker'}
    )
    alumni = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referral_requests_received',
        limit_choices_to={'role': 'alumni'}
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_outcome = models.CharField(
        max_length=20,
        choices=ADMIN_OUTCOME_CHOICES,
        blank=True,
        default=''
    )
    cover_note = models.TextField(
        max_length=1000,
        help_text="Why are you a good fit? (max 1000 chars)"
    )
    alumni_note = models.TextField(
        blank=True,
        help_text="Alumni's note to the requester"
    )
    admin_notes = models.TextField(blank=True, help_text="Admin internal notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['job', 'requester']
        verbose_name = 'Referral Request'
        verbose_name_plural = 'Referral Requests'

    def __str__(self):
        return f"{self.requester.get_full_name()} -> {self.job.title} ({self.status})"

    @property
    def is_pending(self):
        return self.status == 'pending'

    @property
    def is_accepted(self):
        return self.status == 'accepted'

    @property
    def is_rejected(self):
        return self.status == 'rejected'

    def get_status_color(self):
        colors = {
            'pending': 'yellow',
            'accepted': 'green',
            'rejected': 'red',
            'withdrawn': 'gray',
        }
        return colors.get(self.status, 'gray')

    def get_outcome_color(self):
        colors = {
            'hired': 'green',
            'interviewed': 'blue',
            'not_hired': 'red',
            'dropped': 'gray',
        }
        return colors.get(self.admin_outcome, 'gray')
