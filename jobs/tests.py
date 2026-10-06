from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from jobs.models import JobPosting

User = get_user_model()


class JobsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.alumni = User.objects.create_user(
            username='alumni_tester',
            email='alumni_tester@test.com',
            password='testpassword123',
            first_name='Laura',
            last_name='Croft',
            role='alumni'
        )
        self.seeker = User.objects.create_user(
            username='seeker_tester',
            email='seeker_tester@test.com',
            password='testpassword123',
            first_name='Nathan',
            last_name='Drake',
            role='job_seeker'
        )
        self.job = JobPosting.objects.create(
            posted_by=self.alumni,
            title='Staff Security Engineer',
            company='CyberCorp',
            location='Remote',
            employment_type='full_time',
            experience_level='senior',
            description='Lead security architectures and threat response.',
            requirements='5+ years of application security experience.',
            skills_required='AppSec, Cryptography, Python',
            status='active'
        )

    def test_job_listing_public(self):
        response = self.client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Staff Security Engineer')

    def test_job_detail_public(self):
        response = self.client.get(reverse('jobs:detail', args=[self.job.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CyberCorp')

    def test_only_alumni_can_post_job(self):
        # Seeker cannot post
        self.client.force_login(self.seeker)
        response = self.client.post(reverse('jobs:create'), {
            'title': 'Unauthorized Role',
            'company': 'Hax',
            'description': 'Test',
            'requirements': 'Test',
            'employment_type': 'full_time',
            'experience_level': 'entry',
        })
        self.assertEqual(response.status_code, 302)

        # Alumni can post
        self.client.force_login(self.alumni)
        response = self.client.post(reverse('jobs:create'), {
            'title': 'Valid Role',
            'company': 'CyberCorp',
            'description': 'Valid description with sufficient details.',
            'requirements': 'Requirements list.',
            'employment_type': 'full_time',
            'experience_level': 'mid',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(JobPosting.objects.filter(title='Valid Role').exists())
