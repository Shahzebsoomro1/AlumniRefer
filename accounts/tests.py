from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.seeker = User.objects.create_user(
            username='seeker1',
            email='seeker1@test.com',
            password='testpassword123',
            first_name='Alice',
            last_name='Smith',
            role='job_seeker'
        )
        self.alumni = User.objects.create_user(
            username='alumni1',
            email='alumni1@test.com',
            password='testpassword123',
            first_name='Bob',
            last_name='Jones',
            role='alumni'
        )
        self.admin = User.objects.create_superuser(
            username='admin1',
            email='admin1@test.com',
            password='testpassword123',
            first_name='Carol',
            last_name='Admin',
            role='super_admin'
        )

    def test_user_roles(self):
        self.assertTrue(self.seeker.is_job_seeker)
        self.assertFalse(self.seeker.is_alumni)
        self.assertTrue(self.alumni.is_alumni)
        self.assertTrue(self.admin.is_portal_admin)
        self.assertTrue(self.admin.is_super_admin)

    def test_profile_auto_created(self):
        self.assertTrue(hasattr(self.seeker, 'profile'))
        self.assertTrue(hasattr(self.alumni, 'profile'))

    def test_registration_flow(self):
        response = self.client.post(reverse('accounts:register'), {
            'first_name': 'Dave',
            'last_name': 'Williams',
            'email': 'dave@test.com',
            'role': 'job_seeker',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='dave@test.com').exists())

    def test_login_flow(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'seeker1@test.com',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)

    def test_alumni_directory_access(self):
        self.client.force_login(self.seeker)
        response = self.client.get(reverse('accounts:alumni_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bob Jones')
