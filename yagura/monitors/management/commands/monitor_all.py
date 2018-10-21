from django.core.management.base import BaseCommand

from yagura.monitors.services import MonitoringJob
from yagura.sites.models import Site


class Command(BaseCommand):
    help = 'monitor all websites'

    def handle(self, *args, **options):
        # Main
        job = MonitoringJob()
        for site in Site.objects.all():
            job.add_task_form_site(site)
        job.wait_complete()
