from django.db import models
from django.contrib.auth.models import User


class Volunteer(models.Model):

    DISPONIBILITE_CHOICES = [
        ('weekend', 'Weekends'),
        ('semaine', 'En semaine'),
        ('temps_plein', 'Temps plein'),
        ('flexible', 'Flexible'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='volunteer_profile'
    )
    photo = models.ImageField(
        upload_to='volunteers/',
        blank=True, null=True
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Biographie'
    )
    pays = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    telephone = models.CharField(
        max_length=20, blank=True
    )
    competences = models.TextField(
        blank=True,
        verbose_name='Compétences',
        help_text='Ex: informatique, médecine, agriculture'
    )
    langues = models.CharField(
        max_length=200, blank=True,
        help_text='Ex: Français, Anglais, Ewe'
    )
    disponibilite = models.CharField(
        max_length=20,
        choices=DISPONIBILITE_CHOICES,
        default='flexible'
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.ville}"

    class Meta:
        verbose_name = 'Bénévole'
        verbose_name_plural = 'Bénévoles'
        ordering = ['-created_at']


