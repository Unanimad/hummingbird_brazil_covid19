from datetime import datetime

from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.models import Kaggle, Report


def submit_report(date_report):
    instance = Kaggle.objects.last()
    instance.update_kaggle("data/", date_report)


class Command(BaseCommand):
    def handle(self, *args, **options):
        submit_report(datetime.now())
