from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import JobPosting
from .forms import JobPostingForm
from accounts.models import CustomUser


def job_list_view(request):
    """Public job board — all active postings."""
    jobs = JobPosting.objects.filter(status='active').select_related('posted_by', 'posted_by__profile')

    # Filters
    search = request.GET.get('q', '')
    employment_type = request.GET.get('type', '')
    experience = request.GET.get('exp', '')
    location = request.GET.get('loc', '')

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(company__icontains=search) |
            Q(skills_required__icontains=search) |
            Q(description__icontains=search)
        )
    if employment_type:
        jobs = jobs.filter(employment_type=employment_type)
    if experience:
        jobs = jobs.filter(experience_level=experience)
    if location:
        jobs = jobs.filter(location__icontains=location)

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/list.html', {
        'page_obj': page_obj,
        'search': search,
        'employment_type': employment_type,
        'experience': experience,
        'location': location,
        'employment_choices': JobPosting.EMPLOYMENT_TYPE_CHOICES,
        'experience_choices': JobPosting.EXPERIENCE_LEVEL_CHOICES,
    })


def job_detail_view(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    user_referral = None
    if request.user.is_authenticated and request.user.is_job_seeker:
        from referrals.models import ReferralRequest
        user_referral = ReferralRequest.objects.filter(
            job=job, requester=request.user
        ).first()
    return render(request, 'jobs/detail.html', {
        'job': job,
        'user_referral': user_referral,
    })


@login_required
def job_create_view(request):
    if not request.user.is_alumni:
        messages.error(request, "Only alumni can post job openings.")
        return redirect('jobs:list')
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posting published successfully!")
            return redirect('jobs:detail', pk=job.pk)
    else:
        form = JobPostingForm(initial={'company': request.user.profile.company})
    return render(request, 'jobs/create.html', {'form': form})


@login_required
def job_edit_view(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    if job.posted_by != request.user and not request.user.is_portal_admin:
        messages.error(request, "You don't have permission to edit this job.")
        return redirect('jobs:detail', pk=pk)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job posting updated.")
            return redirect('jobs:detail', pk=job.pk)
    else:
        form = JobPostingForm(instance=job)
    return render(request, 'jobs/edit.html', {'form': form, 'job': job})


@login_required
def job_delete_view(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    if job.posted_by != request.user and not request.user.is_portal_admin:
        messages.error(request, "You don't have permission to delete this job.")
        return redirect('jobs:detail', pk=pk)
    if request.method == 'POST':
        job.status = 'removed'
        job.save()
        messages.success(request, "Job posting has been removed.")
        return redirect('jobs:list')
    return render(request, 'jobs/confirm_delete.html', {'job': job})


@login_required
def my_jobs_view(request):
    """Alumni: see my posted jobs."""
    if not request.user.is_alumni:
        return redirect('jobs:list')
    jobs = JobPosting.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})
