from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):

    TYPE_CHOICES = [
        ('ong', 'ONG'),
        ('association', 'Association'),
        ('fondation', 'Fondation'),
        ('gouvernement', 'Gouvernement'),
        ('ecole', 'École'),
        ('hopital', 'Hôpital'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='organization_profile'
    )
    nom = models.CharField(max_length=200)
    logo = models.ImageField(
        upload_to='organizations/',
        blank=True, null=True
    )
    type_org = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='association'
    )
    description = models.TextField()
    pays = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    adresse = models.TextField(blank=True)
    telephone = models.CharField(max_length=20)
    site_web = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisations'
        ordering = ['-created_at']