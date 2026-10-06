from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from jobs.models import JobPosting
from referrals.models import ReferralRequest
from notifications.models import Notification

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds database with realistic corporate alumni, job postings, and referral requests'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Alumni Referral Portal data..."))

        # 1. Super Admin
        admin, created = User.objects.get_or_create(
            email='admin@alumni.com',
            defaults={
                'username': 'admin',
                'first_name': 'System',
                'last_name': 'Admin',
                'role': 'super_admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('adminpassword123')
            admin.save()
            admin.profile.bio = "Corporate Network System Administrator"
            admin.profile.save()
            self.stdout.write(self.style.SUCCESS("Created Super Admin: admin@alumni.com / adminpassword123"))

        # 2. Corporate Alumni
        alumni_data = [
            {
                'email': 'sarah.connor@google.com',
                'username': 'sarah_connor',
                'first_name': 'Sarah',
                'last_name': 'Connor',
                'company': 'Google',
                'job_title': 'Staff Software Engineer',
                'experience': 8,
                'skills': 'Python, Go, Distributed Systems, Kubernetes, GCP',
                'location': 'Mountain View, CA',
                'bio': 'Ex-Meta & Stripe. Currently leading storage infrastructure at Google. Always happy to refer ex-colleagues and ambitious talent.',
                'linkedin': 'https://linkedin.com/in/sarah-connor-demo',
            },
            {
                'email': 'david.chen@microsoft.com',
                'username': 'david_chen',
                'first_name': 'David',
                'last_name': 'Chen',
                'company': 'Microsoft',
                'job_title': 'Principal Product Manager',
                'experience': 10,
                'skills': 'Product Strategy, Cloud Computing, Azure, AI Systems, Agile',
                'location': 'Redmond, WA',
                'bio': '10+ years driving enterprise cloud products. Former corporate alumni champion. Looking to refer high-performing PMs and engineers.',
                'linkedin': 'https://linkedin.com/in/david-chen-demo',
            },
            {
                'email': 'priya.sharma@amazon.com',
                'username': 'priya_sharma',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'company': 'Amazon AWS',
                'job_title': 'Software Engineering Manager',
                'experience': 9,
                'skills': 'Java, Python, AWS Architectures, Team Leadership, Microservices',
                'location': 'New York, NY',
                'bio': 'Managing backend teams at AWS Serverless. Prior alumni team lead. Reach out if you have strong systems experience!',
                'linkedin': 'https://linkedin.com/in/priya-sharma-demo',
            },
            {
                'email': 'alex.rivera@stripe.com',
                'username': 'alex_rivera',
                'first_name': 'Alex',
                'last_name': 'Rivera',
                'company': 'Stripe',
                'job_title': 'Staff Infrastructure Engineer',
                'experience': 7,
                'skills': 'Ruby, Go, PostgreSQL, Kafka, High Availability',
                'location': 'San Francisco, CA (Remote)',
                'bio': 'Focused on global payments reliability. Always excited to support former team members looking for referral into Stripe.',
                'linkedin': 'https://linkedin.com/in/alex-rivera-demo',
            },
        ]

        alumni_users = []
        for data in alumni_data:
            user, u_created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': data['username'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': 'alumni',
                }
            )
            if u_created:
                user.set_password('password123')
                user.save()
            profile = user.profile
            profile.company = data['company']
            profile.job_title = data['job_title']
            profile.years_of_experience = data['experience']
            profile.skills = data['skills']
            profile.location = data['location']
            profile.bio = data['bio']
            profile.linkedin_url = data['linkedin']
            profile.is_verified = True
            profile.is_accepting_referrals = True
            profile.save()
            alumni_users.append(user)

        self.stdout.write(self.style.SUCCESS(f"Created/Verified {len(alumni_users)} Corporate Alumni"))

        # 3. Job Seekers
        seeker_data = [
            {
                'email': 'john.doe@email.com',
                'username': 'john_doe',
                'first_name': 'John',
                'last_name': 'Doe',
                'job_title': 'Senior Full Stack Engineer',
                'company': 'Ex-Corporate Tech',
                'experience': 5,
                'skills': 'Python, Django, React, PostgreSQL, Docker',
                'location': 'Austin, TX',
                'bio': 'Former team member looking for senior engineering opportunities at top tech firms.',
            },
            {
                'email': 'elena.rostova@email.com',
                'username': 'elena_rostova',
                'first_name': 'Elena',
                'last_name': 'Rostova',
                'job_title': 'Frontend Tech Lead',
                'company': 'Ex-Corporate Tech',
                'experience': 6,
                'skills': 'TypeScript, React, Next.js, Tailwind CSS, GraphQL',
                'location': 'Chicago, IL',
                'bio': 'Passionate about design systems and modern web applications. Seeking next leadership role.',
            },
            {
                'email': 'marcus.brody@email.com',
                'username': 'marcus_brody',
                'first_name': 'Marcus',
                'last_name': 'Brody',
                'job_title': 'Cloud DevOps Specialist',
                'company': 'Ex-Corporate Tech',
                'experience': 4,
                'skills': 'AWS, Terraform, CI/CD, Kubernetes, Python',
                'location': 'Remote / Denver, CO',
                'bio': 'Cloud infrastructure automation and reliability engineer.',
            },
        ]

        seeker_users = []
        for data in seeker_data:
            user, u_created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': data['username'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': 'job_seeker',
                }
            )
            if u_created:
                user.set_password('password123')
                user.save()
            profile = user.profile
            profile.company = data['company']
            profile.job_title = data['job_title']
            profile.years_of_experience = data['experience']
            profile.skills = data['skills']
            profile.location = data['location']
            profile.bio = data['bio']
            profile.save()
            seeker_users.append(user)

        self.stdout.write(self.style.SUCCESS(f"Created/Verified {len(seeker_users)} Job Seekers"))

        # 4. Job Postings
        jobs_specs = [
            {
                'alumni_idx': 0,
                'title': 'Senior Backend Engineer (Storage Infrastructure)',
                'company': 'Google',
                'location': 'Mountain View, CA / Hybrid',
                'employment_type': 'full_time',
                'experience_level': 'senior',
                'description': 'Join Google Cloud Storage team building exabyte-scale distributed object storage engines. We are solving challenges around latency, multi-region replication, and fault tolerance.',
                'requirements': '- 5+ years building backend distributed systems in Go or Python.\n- Strong fundamentals in concurrency, networking, and storage algorithms.\n- Experience with Linux internals and production debugging.',
                'skills_required': 'Go, Python, Distributed Systems, Kubernetes, Linux',
                'salary_range': '$180,000 - $240,000 + Equity',
            },
            {
                'alumni_idx': 0,
                'title': 'Site Reliability Engineer (Kubernetes Core)',
                'company': 'Google',
                'location': 'Sunnyvale, CA',
                'employment_type': 'full_time',
                'experience_level': 'senior',
                'description': 'Keep global infrastructure reliable and highly available. Automate cluster lifecycles and build self-healing automation.',
                'requirements': '- 4+ years of SRE or DevOps experience.\n- Deep understanding of Kubernetes architecture.\n- Fluency in Go or Python for infrastructure tooling.',
                'skills_required': 'Kubernetes, SRE, Python, Go, Terraform',
                'salary_range': '$170,000 - $225,000',
            },
            {
                'alumni_idx': 1,
                'title': 'Principal Product Manager - Azure AI Platform',
                'company': 'Microsoft',
                'location': 'Redmond, WA',
                'employment_type': 'full_time',
                'experience_level': 'lead',
                'description': 'Define product direction for next-generation developer tooling on Azure OpenAI services and enterprise model deployment.',
                'requirements': '- 7+ years in product management with cloud or AI platforms.\n- Track record of shipping developer-facing SDKs and enterprise SaaS products.\n- Strong technical background and cross-functional leadership.',
                'skills_required': 'Product Management, Azure, AI/LLMs, Developer Experience',
                'salary_range': '$190,000 - $260,000 + Stock',
            },
            {
                'alumni_idx': 2,
                'title': 'Senior Software Development Engineer (AWS Lambda)',
                'company': 'Amazon AWS',
                'location': 'New York, NY / Hybrid',
                'employment_type': 'full_time',
                'experience_level': 'senior',
                'description': 'Build high-performance control planes for AWS Serverless compute platforms powering billions of requests per second.',
                'requirements': '- 5+ years software engineering experience in Java or Python.\n- Solid understanding of distributed microservice architectures.\n- Obsession with operational excellence and zero-downtime deployments.',
                'skills_required': 'Java, Python, AWS, Microservices, DynamoDB',
                'salary_range': '$175,000 - $230,000',
            },
            {
                'alumni_idx': 3,
                'title': 'Staff Infrastructure Engineer (Payments Core)',
                'company': 'Stripe',
                'location': 'San Francisco, CA (Remote)',
                'employment_type': 'full_time',
                'experience_level': 'senior',
                'description': 'Architect the critical payment processing infrastructure that moves hundreds of billions in GDP every year across 50+ countries.',
                'requirements': '- 6+ years designing mission-critical, transactionally safe distributed systems.\n- Expertise in PostgreSQL query optimization and distributed consensus.\n- Excellent written communication and engineering discipline.',
                'skills_required': 'PostgreSQL, Distributed Systems, Ruby, Go, Kafka',
                'salary_range': '$210,000 - $280,000 + Equity',
            },
            {
                'alumni_idx': 3,
                'title': 'Full Stack Engineer - Merchant Dashboard',
                'company': 'Stripe',
                'location': 'Remote (US / Canada)',
                'employment_type': 'full_time',
                'experience_level': 'mid',
                'description': 'Craft world-class web experiences for millions of business owners and developers managing their finances on Stripe.',
                'requirements': '- 3+ years web development experience with React, TypeScript, and backend APIs.\n- Strong eye for detail, UX polish, and performance.\n- Experience with GraphQL or RESTful services.',
                'skills_required': 'React, TypeScript, GraphQL, Node.js, UI/UX',
                'salary_range': '$150,000 - $195,000',
            },
        ]

        created_jobs = []
        for spec in jobs_specs:
            poster = alumni_users[spec['alumni_idx']]
            job, j_created = JobPosting.objects.get_or_create(
                title=spec['title'],
                company=spec['company'],
                defaults={
                    'posted_by': poster,
                    'location': spec['location'],
                    'employment_type': spec['employment_type'],
                    'experience_level': spec['experience_level'],
                    'description': spec['description'],
                    'requirements': spec['requirements'],
                    'skills_required': spec['skills_required'],
                    'salary_range': spec['salary_range'],
                    'application_deadline': timezone.now().date() + timedelta(days=30),
                    'status': 'active',
                }
            )
            created_jobs.append(job)

        self.stdout.write(self.style.SUCCESS(f"Created/Verified {len(created_jobs)} Job Postings"))

        # 5. Referral Requests with Varied Statuses
        # Ref 1: Accepted & Hired
        ref1, _ = ReferralRequest.objects.get_or_create(
            job=created_jobs[0],
            requester=seeker_users[0],
            defaults={
                'alumni': alumni_users[0],
                'status': 'accepted',
                'admin_outcome': 'hired',
                'cover_note': 'Hi Sarah! Loved working with you on the ex-team. I have spent the last 3 years scaling PostgreSQL & distributed storage systems. Would love an internal referral for this role.',
                'alumni_note': 'John was a stellar teammate on our previous platform team. Highly recommended!',
                'admin_notes': 'Verified alumni employment history. Candidate completed Google interview rounds and accepted offer.',
                'responded_at': timezone.now() - timedelta(days=5),
            }
        )
        created_jobs[0].referrals_count = 1
        created_jobs[0].save()

        # Ref 2: Pending request
        ref2, _ = ReferralRequest.objects.get_or_create(
            job=created_jobs[4],
            requester=seeker_users[0],
            defaults={
                'alumni': alumni_users[3],
                'status': 'pending',
                'cover_note': 'Hi Alex, I have extensive PostgreSQL schema optimization and high-concurrency backend experience. Excited about Stripe Payments!',
            }
        )
        created_jobs[4].referrals_count = 1
        created_jobs[4].save()

        # Ref 3: Accepted (Interviewed)
        ref3, _ = ReferralRequest.objects.get_or_create(
            job=created_jobs[5],
            requester=seeker_users[1],
            defaults={
                'alumni': alumni_users[3],
                'status': 'accepted',
                'admin_outcome': 'interviewed',
                'cover_note': 'Hi Alex! I spearheaded our ex-company design system and complex frontend apps in TypeScript/React. The Merchant Dashboard role fits my background perfectly.',
                'alumni_note': 'Elena has unmatched frontend craft. Submitted referral link through Stripe internal portal.',
                'admin_notes': 'Referral confirmed by referrer. In second stage technical interviews.',
                'responded_at': timezone.now() - timedelta(days=2),
            }
        )
        created_jobs[5].referrals_count = 1
        created_jobs[5].save()

        # 6. In-App Notifications
        Notification.objects.get_or_create(
            recipient=seeker_users[0],
            message="🎉 Congratulations! Your referral for 'Senior Backend Engineer' at Google resulted in an official hire outcome!",
            link="/referrals/my-requests/",
        )
        Notification.objects.get_or_create(
            recipient=alumni_users[3],
            message="John Doe requested a referral for your posting 'Staff Infrastructure Engineer'.",
            link="/referrals/incoming/",
        )
        Notification.objects.get_or_create(
            recipient=seeker_users[1],
            message="Alex Rivera accepted your referral request for 'Full Stack Engineer - Merchant Dashboard'!",
            link="/referrals/my-requests/",
        )

        self.stdout.write(self.style.SUCCESS("Demo database successfully seeded!"))
        self.stdout.write(self.style.NOTICE("""
===================================================================
Default Demo Logins:
- Super Admin: admin@alumni.com / adminpassword123
- Alumni 1:    sarah.connor@google.com / password123
- Alumni 2:    alex.rivera@stripe.com / password123
- Job Seeker:  john.doe@email.com / password123
- Job Seeker 2: elena.rostova@email.com / password123
===================================================================
        """))
