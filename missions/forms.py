from django import forms
from .models import Mission, Candidature


class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = [
            'titre', 'description', 'domaine',
            'image', 'pays', 'ville',
            'places_disponibles', 'duree',
            'competences_requises',
            'date_debut', 'date_fin'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'competences_requises': forms.Textarea(
                attrs={'rows': 3}
            ),
            'date_debut': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'date_fin': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['message']
        widgets = {
            'message': forms.Textarea(
                attrs={
                    'rows': 6,
                    'placeholder':
                        'Explique pourquoi tu veux '
                        'participer à cette mission...'
                }
            )
        }
        labels = {
            'message': 'Lettre de motivation'
        }