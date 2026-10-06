from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import ReferralRequest
from .forms import ReferralRequestForm, AlumniResponseForm, AdminOutcomeForm
from jobs.models import JobPosting
from notifications.utils import send_notification


@login_required
def request_referral_view(request, job_pk):
    """Job Seeker requests a referral for a specific job."""
    if not request.user.is_job_seeker:
        messages.error(request, "Only job seekers can request referrals.")
        return redirect('jobs:detail', pk=job_pk)

    job = get_object_or_404(JobPosting, pk=job_pk, status='active')

    # Check duplicate
    existing = ReferralRequest.objects.filter(job=job, requester=request.user).first()
    if existing:
        messages.warning(request, "You've already requested a referral for this job.")
        return redirect('referrals:my_requests')

    if request.method == 'POST':
        form = ReferralRequestForm(request.POST)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.job = job
            referral.requester = request.user
            referral.alumni = job.posted_by
            referral.save()

            # Update job referral count
            job.referrals_count += 1
            job.save(update_fields=['referrals_count'])

            # Notify the alumni
            send_notification(
                recipient=job.posted_by,
                message=f"{request.user.get_full_name()} has requested a referral for your posting: '{job.title}'.",
                link=f"/referrals/incoming/"
            )

            messages.success(request, "Referral request sent! The alumni will review it shortly.")
            return redirect('referrals:my_requests')
    else:
        form = ReferralRequestForm()

    return render(request, 'referrals/request.html', {'form': form, 'job': job})


@login_required
def my_requests_view(request):
    """Job Seeker: see all referral requests they've made."""
    if not request.user.is_job_seeker:
        return redirect('dashboard:home')
    requests_qs = ReferralRequest.objects.filter(
        requester=request.user
    ).select_related('job', 'alumni', 'alumni__profile')
    return render(request, 'referrals/my_requests.html', {'referral_requests': requests_qs})


@login_required
def withdraw_request_view(request, pk):
    referral = get_object_or_404(ReferralRequest, pk=pk, requester=request.user)
    if referral.status == 'pending':
        referral.status = 'withdrawn'
        referral.save()
        messages.success(request, "Referral request withdrawn.")
    return redirect('referrals:my_requests')


@login_required
def incoming_requests_view(request):
    """Alumni: see referral requests directed at their job postings."""
    if not request.user.is_alumni:
        return redirect('dashboard:home')
    incoming = ReferralRequest.objects.filter(
        alumni=request.user
    ).select_related('requester', 'requester__profile', 'job')

    status_filter = request.GET.get('status', '')
    if status_filter:
        incoming = incoming.filter(status=status_filter)

    return render(request, 'referrals/incoming.html', {
        'referral_requests': incoming,
        'status_filter': status_filter,
    })


@login_required
def respond_to_request_view(request, pk):
    """Alumni: accept or reject a referral request."""
    referral = get_object_or_404(ReferralRequest, pk=pk, alumni=request.user)
    if referral.status != 'pending':
        messages.warning(request, "This request has already been responded to.")
        return redirect('referrals:incoming')

    if request.method == 'POST':
        form = AlumniResponseForm(request.POST, instance=referral)
        if form.is_valid():
            ref = form.save(commit=False)
            ref.responded_at = timezone.now()
            ref.save()

            action = "accepted" if ref.status == 'accepted' else "declined"
            send_notification(
                recipient=referral.requester,
                message=f"{request.user.get_full_name()} has {action} your referral request for '{referral.job.title}'.",
                link=f"/referrals/my-requests/"
            )
            messages.success(request, f"Referral request {action}.")
            return redirect('referrals:incoming')
    else:
        form = AlumniResponseForm(instance=referral)

    return render(request, 'referrals/respond.html', {'form': form, 'referral': referral})


@login_required
def admin_manage_view(request):
    """Admin: overview of all referral requests with outcome marking."""
    if not request.user.is_portal_admin:
        messages.error(request, "Access denied.")
        return redirect('dashboard:home')

    all_referrals = ReferralRequest.objects.select_related(
        'job', 'requester', 'requester__profile', 'alumni', 'alumni__profile'
    ).order_by('-created_at')

    status_filter = request.GET.get('status', '')
    outcome_filter = request.GET.get('outcome', '')
    if status_filter:
        all_referrals = all_referrals.filter(status=status_filter)
    if outcome_filter:
        all_referrals = all_referrals.filter(admin_outcome=outcome_filter)

    return render(request, 'referrals/admin_manage.html', {
        'all_referrals': all_referrals,
        'status_filter': status_filter,
        'outcome_filter': outcome_filter,
        'outcome_choices': ReferralRequest.ADMIN_OUTCOME_CHOICES,
    })


@login_required
def mark_outcome_view(request, pk):
    """Admin: mark outcome of a referral request."""
    if not request.user.is_portal_admin:
        messages.error(request, "Access denied.")
        return redirect('dashboard:home')

    referral = get_object_or_404(ReferralRequest, pk=pk)
    if request.method == 'POST':
        form = AdminOutcomeForm(request.POST, instance=referral)
        if form.is_valid():
            form.save()
            messages.success(request, "Outcome updated successfully.")
            return redirect('referrals:admin_manage')
    else:
        form = AdminOutcomeForm(instance=referral)

    return render(request, 'referrals/mark_outcome.html', {'form': form, 'referral': referral})
