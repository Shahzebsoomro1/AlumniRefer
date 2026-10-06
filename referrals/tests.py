from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from jobs.models import JobPosting
from referrals.models import ReferralRequest
from notifications.models import Notification

User = get_user_model()


class ReferralWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.alumni = User.objects.create_user(
            username='alumni_ref',
            email='alumni_ref@test.com',
            password='testpassword123',
            first_name='Bruce',
            last_name='Wayne',
            role='alumni'
        )
        self.seeker = User.objects.create_user(
            username='seeker_ref',
            email='seeker_ref@test.com',
            password='testpassword123',
            first_name='Dick',
            last_name='Grayson',
            role='job_seeker'
        )
        self.admin = User.objects.create_superuser(
            username='admin_ref',
            email='admin_ref@test.com',
            password='testpassword123',
            first_name='Jim',
            last_name='Gordon',
            role='super_admin'
        )
        self.job = JobPosting.objects.create(
            posted_by=self.alumni,
            title='Lead Detective',
            company='Wayne Enterprises',
            employment_type='full_time',
            experience_level='senior',
            description='Investigation and high-level strategy.',
            requirements='Relevant experience in field analysis.',
            status='active'
        )

    def test_complete_referral_lifecycle(self):
        # 1. Seeker requests referral
        self.client.force_login(self.seeker)
        request_response = self.client.post(reverse('referrals:request', args=[self.job.pk]), {
            'cover_note': 'I have 5 years of detective experience and worked closely with the team.'
        })
        self.assertEqual(request_response.status_code, 302)

        referral = ReferralRequest.objects.filter(job=self.job, requester=self.seeker).first()
        self.assertIsNotNone(referral)
        self.assertEqual(referral.status, 'pending')

        # Alumni received in-app notification
        alumni_notif = Notification.objects.filter(recipient=self.alumni).first()
        self.assertIsNotNone(alumni_notif)
        self.assertIn('requested a referral', alumni_notif.message)

        # 2. Alumni reviews and accepts referral
        self.client.force_login(self.alumni)
        respond_response = self.client.post(reverse('referrals:respond', args=[referral.pk]), {
            'status': 'accepted',
            'alumni_note': 'Submitted referral to Wayne HR portal.'
        })
        self.assertEqual(respond_response.status_code, 302)

        referral.refresh_from_db()
        self.assertEqual(referral.status, 'accepted')

        # Seeker received in-app notification
        seeker_notif = Notification.objects.filter(recipient=self.seeker).first()
        self.assertIsNotNone(seeker_notif)
        self.assertIn('accepted', seeker_notif.message)

        # 3. Admin marks final hiring outcome
        self.client.force_login(self.admin)
        outcome_response = self.client.post(reverse('referrals:mark_outcome', args=[referral.pk]), {
            'admin_outcome': 'hired',
            'admin_notes': 'Candidate accepted offer. Background check passed.'
        })
        self.assertEqual(outcome_response.status_code, 302)

        referral.refresh_from_db()
        self.assertEqual(referral.admin_outcome, 'hired')
        self.assertEqual(referral.admin_notes, 'Candidate accepted offer. Background check passed.')
