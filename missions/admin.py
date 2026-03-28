from django.contrib import admin
from .models import Mission, Candidature


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = [
        'titre', 'organisation', 'domaine',
        'pays', 'statut', 'places_disponibles',
        'created_at'
    ]
    list_filter = ['statut', 'domaine', 'pays']
    search_fields = ['titre', 'description']
    prepopulated_fields = {'slug': ('titre',)}
    list_editable = ['statut']


@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = [
        'volunteer', 'mission', 'statut', 'created_at'
    ]
    list_filter = ['statut']
    list_editable = ['statut']