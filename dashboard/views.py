from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from jobs.models import JobPosting
from referrals.models import ReferralRequest
from accounts.models import CustomUser
from notifications.models import Notification


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    featured_jobs = JobPosting.objects.filter(status='active').select_related('posted_by')[:6]
    stats = {
        'total_jobs': JobPosting.objects.filter(status='active').count(),
        'total_alumni': CustomUser.objects.filter(role='alumni').count(),
        'total_referrals': ReferralRequest.objects.count(),
        'total_hired': ReferralRequest.objects.filter(admin_outcome='hired').count(),
    }
    return render(request, 'dashboard/landing.html', {
        'featured_jobs': featured_jobs,
        'stats': stats,
    })



@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}

    if user.is_job_seeker:
        my_requests = ReferralRequest.objects.filter(requester=user).select_related('job', 'alumni')
        active_jobs = JobPosting.objects.filter(status='active').count()
        context.update({
            'my_requests': my_requests[:5],
            'total_requests': my_requests.count(),
            'pending_count': my_requests.filter(status='pending').count(),
            'accepted_count': my_requests.filter(status='accepted').count(),
            'rejected_count': my_requests.filter(status='rejected').count(),
            'active_jobs_count': active_jobs,
        })

    elif user.is_alumni:
        my_jobs = JobPosting.objects.filter(posted_by=user)
        incoming = ReferralRequest.objects.filter(alumni=user).select_related('requester', 'job')
        context.update({
            'my_jobs': my_jobs[:5],
            'total_jobs': my_jobs.count(),
            'active_jobs': my_jobs.filter(status='active').count(),
            'incoming_requests': incoming[:5],
            'total_incoming': incoming.count(),
            'pending_incoming': incoming.filter(status='pending').count(),
            'accepted_incoming': incoming.filter(status='accepted').count(),
        })

    elif user.is_portal_admin:
        all_referrals = ReferralRequest.objects.all()
        all_users = CustomUser.objects.all()
        all_jobs = JobPosting.objects.all()
        context.update({
            'total_users': all_users.count(),
            'total_alumni': all_users.filter(role='alumni').count(),
            'total_seekers': all_users.filter(role='job_seeker').count(),
            'total_jobs': all_jobs.count(),
            'active_jobs': all_jobs.filter(status='active').count(),
            'total_referrals': all_referrals.count(),
            'pending_referrals': all_referrals.filter(status='pending').count(),
            'accepted_referrals': all_referrals.filter(status='accepted').count(),
            'hired_count': all_referrals.filter(admin_outcome='hired').count(),
            'recent_referrals': all_referrals.order_by('-created_at')[:8],
            'recent_jobs': all_jobs.order_by('-created_at')[:5],
            'recent_users': all_users.order_by('-date_joined')[:5],
        })

    return render(request, 'dashboard/dashboard.html', context)
