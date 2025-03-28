import os
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from goats.models import Goat  # Adjust import based on your model location

class Command(BaseCommand):
    help = 'Migrate local goat images to Cloudinary'

    def handle(self, *args, **options):
        for goat in Goat.objects.exclude(image__isnull=True).exclude(image__exact=''):
            if goat.image.name.startswith(('http://', 'https://')):
                self.stdout.write(f'Skipped {goat.name} (already migrated)')
                continue
            
            try:
                with goat.image.open('rb') as f:
                    default_storage.save(goat.image.name, f)
                self.stdout.write(f'Success: {goat.name} ({goat.image.name})')
            except Exception as e:
                self.stderr.write(f'Failed {goat.name}: {str(e)}')