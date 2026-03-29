from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Crée le superuser automatiquement'

    def handle(self, *args, **kwargs):
        username = os.getenv(
            'DJANGO_SUPERUSER_USERNAME', 'GOSHEN'
        )
        email = os.getenv(
            'DJANGO_SUPERUSER_EMAIL', 'admin@example.com'
        )
        password = os.getenv(
            'DJANGO_SUPERUSER_PASSWORD', '@admin123'
        )

        if not User.objects.filter(
            username=username
        ).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Superuser "{username}" créé !'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️ Superuser "{username}" existe déjà.'
                )
            )