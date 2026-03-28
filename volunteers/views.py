from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Volunteer
from .forms import VolunteerRegisterForm, VolunteerProfileForm


def register(request):
    if request.method == 'POST':
        form = VolunteerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Volunteer.objects.create(
                user=user,
                pays=form.cleaned_data.get('pays', ''),
                ville=form.cleaned_data.get('ville', ''),
            )
            login(request, user)
            messages.success(
                request,
                "Compte créé ! Bienvenue "
            )
            return redirect('volunteer_dashboard')
    else:
        form = VolunteerRegisterForm()

    return render(request, 'volunteers/register.html', {
        'form': form
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user:
            login(request, user)
            return redirect('volunteer_dashboard')
        else:
            messages.error(
                request,
                "Identifiants incorrects."
            )
    return render(request, 'volunteers/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    try:
        volunteer = request.user.volunteer_profile
        candidatures = volunteer.candidatures.all()
    except Exception:
        return redirect('volunteer_profile_edit')

    return render(
        request, 'volunteers/dashboard.html', {
            'volunteer': volunteer,
            'candidatures': candidatures,
        }
    )


@login_required
def profile_edit(request):
    try:
        volunteer = request.user.volunteer_profile
    except Exception:
        volunteer = Volunteer(user=request.user)

    if request.method == 'POST':
        form = VolunteerProfileForm(
            request.POST,
            request.FILES,
            instance=volunteer
        )
        if form.is_valid():
            form.save()
            messages.success(
                request, "Profil mis à jour "
            )
            return redirect('volunteer_dashboard')
    else:
        form = VolunteerProfileForm(instance=volunteer)

    return render(
        request, 'volunteers/profile_edit.html', {
            'form': form
        }
    )