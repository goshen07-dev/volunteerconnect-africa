from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Organization
from .forms import OrganizationRegisterForm, OrganizationProfileForm


def organization_list(request):
    organizations = Organization.objects.filter(
        is_verified=True
    ).order_by('-created_at')

    return render(
        request,
        'organizations/list.html',
        {'organizations': organizations}
    )


def organization_register(request):
    if request.method == 'POST':
        form = OrganizationRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            Organization.objects.create(
                user=user,
                nom=form.cleaned_data['nom'],
                type_org=form.cleaned_data['type_org'],
                description=form.cleaned_data['description'],
                pays=form.cleaned_data['pays'],
                ville=form.cleaned_data['ville'],
                telephone=form.cleaned_data['telephone'],
            )
            login(request, user)
            messages.success(
                request,
                "Organisation créée ! En attente de vérification. "
            )
            return redirect('organization_dashboard')
    else:
        form = OrganizationRegisterForm()

    return render(
        request,
        'organizations/register.html',
        {'form': form}
    )


@login_required
def organization_dashboard(request):
    try:
        organization = request.user.organization_profile
        missions = organization.missions.all()
    except Exception:
        return redirect('organization_register')

    return render(
        request,
        'organizations/dashboard.html',
        {
            'organization': organization,
            'missions': missions,
        }
    )


@login_required
def mission_create(request):
    from missions.forms import MissionForm

    try:
        organization = request.user.organization_profile
    except Exception:
        messages.error(
            request,
            "Complète ton profil organisation d'abord."
        )
        return redirect('organization_register')

    if request.method == 'POST':
        form = MissionForm(request.POST, request.FILES)
        if form.is_valid():
            mission = form.save(commit=False)
            mission.organisation = organization
            mission.save()
            messages.success(
                request,
                "Mission créée avec succès ! "
            )
            return redirect('organization_dashboard')
    else:
        form = MissionForm()

    return render(
        request,
        'missions/create.html',
        {'form': form}
    )