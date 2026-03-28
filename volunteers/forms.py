from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Volunteer


class VolunteerRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        max_length=100, required=True,
        label='Prénom'
    )
    last_name = forms.CharField(
        max_length=100, required=True,
        label='Nom'
    )
    pays = forms.CharField(
        max_length=100, required=True,
        label='Pays'
    )
    ville = forms.CharField(
        max_length=100, required=True,
        label='Ville'
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'pays', 'ville',
            'password1', 'password2'
        ]


class VolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = [
            'photo', 'bio', 'pays', 'ville',
            'telephone', 'competences',
            'langues', 'disponibilite'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'competences': forms.Textarea(attrs={'rows': 3}),
        }