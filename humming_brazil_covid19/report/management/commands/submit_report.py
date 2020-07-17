from datetime import datetime

from django.core.management.base import BaseCommand
from kaggle import KaggleApi

from humming_brazil_covid19.report.models import Kaggle, Report


def submit_report(date_report):
    api = KaggleApi()
    api.authenticate()

    last_update = datetime.strftime(date_report, "%m/%d/%Y %H:%M")
    api.dataset_create_version(
        "data/", f"Auto update - {last_update} GMT-3", delete_old_versions=True
    )


class Command(BaseCommand):
    def handle(self, *args, **options):
        submit_report(datetime.now())
