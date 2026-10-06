# 🎓 AlumniRefer — Corporate Alumni Job Referral Portal

A modern, full-stack **Corporate Alumni Job Referral Network** built with **Django**, **PostgreSQL**, **Tailwind CSS**, and **Alpine.js**.

Designed and architected end-to-end to connect ex-employees at top companies with former colleagues seeking direct job referrals, complete with administrator verification and hiring outcome tracking.

---

## 🌟 Core Value Proposition

- **No Resume Black Holes**: Job seekers get direct employee referrals 
- **Alumni Engagement**: Corporate alumni give back to their former network while earning company referral bonuses.
- **Admin Moderation & Governance**: Platform administrators oversee the referral pipeline, eliminate spam, and track actual hiring outcomes (*Interviewed*, *Hired*, *Not Hired*).

---

## 🚀 Key Features

| Role | Capabilities |
|---|---|
| **Job Seeker (Candidate)** | • Browse active corporate openings with multi-criteria search (type, level, keywords)<br>• Submit personalized referral requests with cover notes directly to alumni posters<br>• Real-time request status tracking (*Pending*, *Accepted*, *Declined*, *Hired*)<br>• Browse the verified Alumni Directory and connect with ex-colleagues |
| **Alumni (Referrer)** | • Post openings from current company with salary, skills, and deadlines<br>• Manage incoming referral requests with full candidate profile view<br>• Accept or decline requests with custom feedback notes<br>• Toggle availability (*Open to referrals*) on public profile |
| **Admin & Super Admin** | • Unified Referral Management dashboard with status & outcome filters<br>• Record and verify official hiring outcomes (*Hired*, *Interviewed*, *Candidate Dropped*)<br>• Moderate/remove job postings<br>• Full Django Admin panel integration with customized user and inline profile management |
| **All Users** | • In-app notification center with unread bell counter and click-to-view navigation<br>• Rich profile customization (avatar, bio, company, experience, skills tags, LinkedIn URL)<br>• Clean, modern Tailwind CSS design system with responsive layouts |

---

## 🏗️ Architecture & Technology Stack

- **Backend**: Python 3.14 / Django 6.1
- **Database**:
  - **PostgreSQL** via `psycopg2-binary` (production-ready)
  - **SQLite** fallback for zero-configuration instant local development
- **Frontend**: Django Templates + Tailwind CSS (custom Indigo/Brand palette) + Alpine.js
- **Form Handling**: Django Forms + `crispy-forms` + `crispy-tailwind`
- **Authentication**: Custom User model (`accounts.CustomUser`) using email as username
- **Signals**: Automatic 1-to-1 Profile instantiation upon user registration

---

## 📁 Project Directory Structure

```text
alumni_referral_portal/
├── config/
│   ├── settings.py           # Database toggle, installed apps, crispy config
│   ├── urls.py               # Root URL router
│   ├── wsgi.py               # WSGI application entry
│   └── __init__.py
├── accounts/
│   ├── models.py             # CustomUser (roles) & Profile models
│   ├── forms.py              # RegisterForm, CustomLoginForm, ProfileForm
│   ├── views.py              # Auth, profile, and alumni directory views
│   ├── signals.py            # Auto profile creation signal
│   ├── admin.py              # UserAdmin with inline Profile editor
│   ├── tests.py              # Unit tests for accounts & auth
│   └── management/commands/
│       └── seed_data.py      # Demo dataset seeder
├── jobs/
│   ├── models.py             # JobPosting model
│   ├── forms.py              # JobPostingForm
│   ├── views.py              # List, detail, create, edit, delete, my_jobs
│   ├── admin.py              # Job admin with bulk moderation actions
│   └── tests.py              # Unit tests for job posting & permissions
├── referrals/
│   ├── models.py             # ReferralRequest model (statuses & outcomes)
│   ├── forms.py              # Request, response, and admin outcome forms
│   ├── views.py              # Request, respond, withdraw, admin manage
│   ├── admin.py              # ReferralRequest admin
│   └── tests.py              # Integration test for the 3-party workflow
├── notifications/
│   ├── models.py             # In-app Notification model
│   ├── utils.py              # send_notification helper
│   ├── context_processors.py # Injects unread count globally
│   └── views.py              # Notification list and mark-as-read
├── dashboard/
│   ├── views.py              # Public landing page + role-based dashboards
│   └── urls.py               # Dashboard routes
├── templates/
│   ├── base.html             # Master layout, navbar, notifications dropdown
│   ├── accounts/             # Login, register, profile, alumni directory
│   ├── jobs/                 # Job board, job details, job create/edit
│   ├── referrals/            # Request form, my requests, incoming, admin manage
│   ├── dashboard/            # High-converting landing page & role dashboards
│   └── notifications/        # Notification center
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── manage.py                 # Django CLI
```

---

## ⚡ Quickstart Guide

### 1. Activate Virtual Environment
From PowerShell in the project directory:
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Apply Migrations
```powershell
python manage.py migrate
```

### 3. Seed Realistic Demo Data
Populates corporate alumni from Google, Microsoft, Stripe, Amazon, active job openings, and referral requests:
```powershell
python manage.py seed_data
```

### 4. Run Development Server
```powershell
python manage.py runserver
```
Visit **http://127.0.0.1:8000** in your browser.

---

## 🔑 Pre-Seeded Demo Accounts

You can log in immediately with any of these pre-configured accounts:

| Role | Email | Password | Details |
|---|---|---|---|
| **Super Admin** | `admin@alumni.com` | `adminpassword123` | Access to `/dashboard/`, `/referrals/admin/manage/`, and `/admin/` |
| **Alumni (Google)** | `sarah.connor@google.com` | `password123` | Staff Engineer at Google with active openings |
| **Alumni (Stripe)** | `alex.rivera@stripe.com` | `password123` | Staff Infra Engineer with active openings & requests |
| **Alumni (Microsoft)**| `david.chen@microsoft.com` | `password123` | Principal PM with active openings |
| **Job Seeker 1** | `john.doe@email.com` | `password123` | Has active and hired referral requests |
| **Job Seeker 2** | `elena.rostova@email.com` | `password123` | Frontend Tech Lead seeking referrals |

---

## 🐘 Switching to PostgreSQL

To connect to a live PostgreSQL instance:

1. Ensure PostgreSQL is running locally or via Docker:
   ```bash
   docker run --name alumni-postgres -e POSTGRES_DB=alumni_portal_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
   ```
2. Enable PostgreSQL in your environment:
   ```powershell
   $env:USE_POSTGRES = "True"
   $env:POSTGRES_DB = "alumni_portal_db"
   $env:POSTGRES_USER = "postgres"
   $env:POSTGRES_PASSWORD = "postgres"
   $env:POSTGRES_HOST = "localhost"
   $env:POSTGRES_PORT = "5432"
   ```
3. Run migrations and seed data:
   ```powershell
   python manage.py migrate
   python manage.py seed_data
   ```

---

## 🧪 Running Automated Tests

Run the full Django test suite verifying accounts, authentication, jobs, permissions, and referral workflows:
```powershell
python manage.py test
```
Result: **9 tests, 100% passing.**
