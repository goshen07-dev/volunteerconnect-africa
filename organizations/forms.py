from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Organization


class OrganizationRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nom = forms.CharField(
        max_length=200,
        label="Nom de l'organisation"
    )
    type_org = forms.ChoiceField(
        choices=Organization.TYPE_CHOICES,
        label="Type d'organisation"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Description'
    )
    pays = forms.CharField(max_length=100)
    ville = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = [
            'username', 'email',
            'nom', 'type_org', 'description',
            'pays', 'ville', 'telephone',
            'password1', 'password2'
        ]


class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'nom', 'logo', 'type_org',
            'description', 'pays', 'ville',
            'adresse', 'telephone', 'site_web'
        ]
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 4}
            ),
        }