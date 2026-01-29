from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from alumni_sos.models import SOSRequest

class Command(BaseCommand):
    help = 'Deletes SOS requests older than 48 hours'

    def handle(self, *args, **kwargs):
        expired_requests = SOSRequest.objects.filter(deadline__lt=timezone.now())
        count = expired_requests.count()
        expired_requests.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired SOS requests.'))
