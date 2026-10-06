from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterForm, CustomLoginForm, ProfileForm
from .models import CustomUser, Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}! Your account has been created.")
            return redirect('dashboard:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You've been logged out successfully.")
    return redirect('accounts:login')


@login_required
def profile_view(request, pk=None):
    if pk:
        user = get_object_or_404(CustomUser, pk=pk)
    else:
        user = request.user
    profile = user.profile
    return render(request, 'accounts/profile.html', {'profile_user': user, 'profile': profile})


@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def alumni_list_view(request):
    """Public list of alumni who accept referrals."""
    alumni = CustomUser.objects.filter(
        role='alumni',
        profile__is_accepting_referrals=True
    ).select_related('profile').order_by('-date_joined')

    search = request.GET.get('q', '')
    company = request.GET.get('company', '')
    if search:
        alumni = alumni.filter(
            profile__skills__icontains=search
        ) | alumni.filter(
            profile__job_title__icontains=search
        )
    if company:
        alumni = alumni.filter(profile__company__icontains=company)

    return render(request, 'accounts/alumni_list.html', {
        'alumni': alumni,
        'search': search,
        'company': company
    })
