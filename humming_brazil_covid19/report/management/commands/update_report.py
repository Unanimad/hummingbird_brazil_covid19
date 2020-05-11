import json

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.models import *
from humming_brazil_covid19.report.utils import to_csv

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

    request = requests.get(url + "PortalGeralApi", headers=headers)
    content = request.content.decode("utf8")
    data = json.loads(content)

    last_report = datetime.strptime(data["dt_updated"], '%Y-%m-%dT%H:%M:%S.%fZ')

    report, created = Report.objects.get_or_create(updated_at=last_report)

    if not created:
        print(f"Novo relatório encontrado em {last_report}")
        request = requests.get(url + "PortalEstado", headers=headers)
        content = request.content.decode("utf8")
        data = json.loads(content)

        for state in data:
            case = list(Case.objects.filter(state=state["nome"]))[0]

            cases = state.get("casosAcumulado", 0)
            deaths = state.get("obitosAcumulado", 0)

            Case.objects.get_or_create(
                cases=cases,
                deaths=deaths,
                state=state["nome"],
                region=case.region,
                report=report,
            )

        request = requests.get(url + "PortalMunicipio", headers=headers)
        content = request.content.decode("utf8")
        data = json.loads(content)

        for city in data:
            try:
                instance = list(CityCase.objects.filter(code=city["cod"]))[0]
            except:
                print(city)
                continue
            else:
                cases = city.get("casosAcumulado", 0)
                deaths = city.get("obitosAcumulado", 0)

                CityCase.objects.get_or_create(
                    cases=cases,
                    deaths=deaths,
                    name=instance.name,
                    code=instance.code,
                    state=instance.state,
                    report=report,
                )

        to_csv()

        instance = Kaggle.objects.last()
        if not instance:
            instance = Kaggle.objects.create(last_update=last_report)

        instance.update_kaggle("data/", last_report)

    else:
        print(f"The last report {report.updated_at} already exists!")

    print(f"Done! The time is: {datetime.now()}")


class Command(BaseCommand):
    help = "Automatically update  kaggle dataset with the last cases of COVID-19 in Brazil."

    def handle(self, *args, **options):
        print("Cron started! Wait the job starts!")

        scheduler = BlockingScheduler()
        scheduler.add_job(cron, "cron", hour=20, timezone="America/Maceio")

        scheduler.start()
