from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Mission, Candidature
from .forms import MissionForm, CandidatureForm


def home(request):
    missions = Mission.objects.filter(
        statut='ouverte'
    ).order_by('-created_at')[:6]

    total_missions = Mission.objects.filter(
        statut='ouverte'
    ).count()

    from volunteers.models import Volunteer
    total_benevoles = Volunteer.objects.count()

    from organizations.models import Organization
    total_orgs = Organization.objects.count()

    domaines = Mission.DOMAINE_CHOICES

    context = {
        'missions': missions,
        'total_missions': total_missions,
        'total_benevoles': total_benevoles,
        'total_orgs': total_orgs,
        'domaines': domaines,
    }
    return render(request, 'home.html', context)


def mission_list(request):
    missions = Mission.objects.filter(statut='ouverte')

    domaine = request.GET.get('domaine')
    pays = request.GET.get('pays')
    query = request.GET.get('q')

    if domaine:
        missions = missions.filter(domaine=domaine)
    if pays:
        missions = missions.filter(pays__icontains=pays)
    if query:
        missions = missions.filter(
            Q(titre__icontains=query) |
            Q(description__icontains=query) |
            Q(ville__icontains=query)
        )

    context = {
        'missions': missions,
        'domaines': Mission.DOMAINE_CHOICES,
        'domaine_actif': domaine,
        'query': query or '',
    }
    return render(request, 'missions/list.html', context)


def mission_detail(request, slug):
    mission = get_object_or_404(Mission, slug=slug)

    deja_candidat = False
    if request.user.is_authenticated:
        try:
            volunteer = request.user.volunteer_profile
            deja_candidat = Candidature.objects.filter(
                mission=mission,
                volunteer=volunteer
            ).exists()
        except Exception:
            pass

    context = {
        'mission': mission,
        'deja_candidat': deja_candidat,
    }
    return render(
        request, 'missions/detail.html', context
    )


@login_required
def postuler(request, slug):
    mission = get_object_or_404(
        Mission, slug=slug, statut='ouverte'
    )

    try:
        volunteer = request.user.volunteer_profile
    except Exception:
        messages.error(
            request,
            "Complète ton profil bénévole d'abord."
        )
        return redirect('volunteer_profile_edit')

    if Candidature.objects.filter(
        mission=mission, volunteer=volunteer
    ).exists():
        messages.warning(
            request, "Tu as déjà postulé à cette mission."
        )
        return redirect('mission_detail', slug=slug)

    if request.method == 'POST':
        form = CandidatureForm(request.POST)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.mission = mission
            candidature.volunteer = volunteer
            candidature.save()
            messages.success(
                request,
                "Candidature envoyée avec succès ! "
            )
            return redirect('mission_detail', slug=slug)
    else:
        form = CandidatureForm()

    return render(request, 'missions/postuler.html', {
        'mission': mission,
        'form': form,
    })