import json

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.management.commands.split_database import split_database
from humming_brazil_covid19.report.management.commands.submit_report import submit_report
from humming_brazil_covid19.report.models import *

url = "https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/"
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-parse-application-id": "unAFkcaNDeXajurGB7LChj8SgQYS2ptm",
}


def cron(*args, **options):
    print(f"Cron job is running. The time is {datetime.now()}")

    request = requests.get(url + "PortalGeral", headers=headers)
    content = request.content.decode("utf8")
    data = json.loads(content)['results'][0]

    last_report = datetime.strptime(data["dt_atualizacao"], "%d/%m/%Y %H:%M")

    split_database()
    submit_report(last_report)

    print(f"Done! The time is: {datetime.now()}")


class Command(BaseCommand):
    help = "Automatically update  kaggle dataset with the last cases of COVID-19 in Brazil."

    def handle(self, *args, **options):
        print("Cron started! Wait the job starts!")

        scheduler = BlockingScheduler()
        scheduler.add_job(cron, "cron", hour=20, timezone="America/Maceio")

        scheduler.start()
