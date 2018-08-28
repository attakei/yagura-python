from uuid import UUID

from django.core.management.base import BaseCommand, CommandError

from yagura.monitors.services import MonitoringJob
from yagura.sites.models import Site


class Command(BaseCommand):
    help = 'monitor specified website'

    def add_arguments(self, parser):
        parser.add_argument('site_id', type=str)

    def handle(self, *args, **options):
        site_id = options['site_id']
        # Validation
        try:
            UUID(site_id)
        except ValueError:
            raise CommandError(f"Argument must be UUID")
        # Main
        try:
            site = Site.objects.get(pk=site_id)
        except Site.DoesNotExist:
            raise CommandError(f"Site is not found")
        job = MonitoringJob()
        job.add_task_form_site(site)
        job.wait_complete()
