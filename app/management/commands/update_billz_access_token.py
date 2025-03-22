from django.core.management.base import BaseCommand
from app.scheduled_job.billz_job import fetch_and_cache_access_token

class Command(BaseCommand):
    help = 'Fetch and cache Billz access token'

    def handle(self, *args, **kwargs):
        fetch_and_cache_access_token()
        self.stdout.write(self.style.SUCCESS('Successfully updated Billz access token'))
