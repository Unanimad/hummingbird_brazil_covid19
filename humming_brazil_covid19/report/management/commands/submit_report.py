from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.models import Kaggle, Report


def submit_report():
    instance = Kaggle.objects.last()
    if not instance:
        last_report = Report.objects.last()
        instance = Kaggle.objects.create(last_update=last_report.updated_at)

    instance.update_kaggle("data/", last_report.updated_at)


class Command(BaseCommand):
    def handle(self, *args, **options):
        submit_report()
