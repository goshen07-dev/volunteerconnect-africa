from django.db import models
from organizations.models import Organization
from volunteers.models import Volunteer


class Mission(models.Model):

    DOMAINE_CHOICES = [
        ('education', 'Éducation'),
        ('sante', 'Santé'),
        ('environnement', 'Environnement'),
        ('tech', 'Technologie'),
        ('agriculture', 'Agriculture'),
        ('droits', 'Droits humains'),
        ('sport', 'Sport'),
        ('culture', 'Culture & Arts'),
        ('autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('ouverte', 'Ouverte'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    DUREE_CHOICES = [
        ('1_semaine', '1 semaine'),
        ('2_semaines', '2 semaines'),
        ('1_mois', '1 mois'),
        ('3_mois', '3 mois'),
        ('6_mois', '6 mois'),
        ('1_an', '1 an ou plus'),
    ]

    organisation = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='missions'
    )
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    domaine = models.CharField(
        max_length=20,
        choices=DOMAINE_CHOICES
    )
    image = models.ImageField(
        upload_to='missions/',
        blank=True, null=True
    )
    pays = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    places_disponibles = models.PositiveIntegerField(default=1)
    duree = models.CharField(
        max_length=20,
        choices=DUREE_CHOICES
    )
    competences_requises = models.TextField(blank=True)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='ouverte'
    )
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def places_restantes(self):
        prises = self.candidatures.filter(
            statut='acceptee'
        ).count()
        return self.places_disponibles - prises

    class Meta:
        verbose_name = 'Mission'
        verbose_name_plural = 'Missions'
        ordering = ['-created_at']


class Candidature(models.Model):

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    ]

    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name='candidatures'
    )
    volunteer = models.ForeignKey(
        Volunteer,
        on_delete=models.CASCADE,
        related_name='candidatures'
    )
    message = models.TextField(
        verbose_name='Lettre de motivation'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.volunteer} → {self.mission.titre}"
        )

    class Meta:
        verbose_name = 'Candidature'
        verbose_name_plural = 'Candidatures'
        unique_together = ['mission', 'volunteer']
        ordering = ['-created_at']