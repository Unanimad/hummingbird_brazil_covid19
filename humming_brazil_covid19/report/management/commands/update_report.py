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

    request = requests.get(url + "PortalGeral", headers=headers)
    content = request.content.decode("utf8")
    data = json.loads(content)['results'][0]

    last_report = datetime.strptime(data["dt_atualizacao"], "%d/%m/%Y %H:%M")

    report, created = Report.objects.get_or_create(updated_at=last_report)

    if not created:
        print(f"Novo relatório encontrado em {last_report}")

        request = requests.get(url + "PortalSintese", headers=headers)
        content = request.content.decode("utf8")
        data = json.loads(content)
        data = data[0]

        if data["coduf"] == "76":
            cases = data['casosAcumulado']
            deaths = data['obitosAcumulado']
            week = data['semanaEpi']
            recovered = data['Recuperadosnovos']
            monitoring = data['emAcompanhamentoNovos']

            MacroCase.objects.get_or_create(
                cases=cases, deaths=deaths, week=week,
                recovered=recovered, monitoring=monitoring, report=report
            )

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
            cases = city.get("casosAcumulado", 0)
            deaths = city.get("obitosAcumulado", 0)
            state = CityCase.UF_CODE[city['cod'][:2]]

            CityCase.objects.get_or_create(
                cases=cases,
                deaths=deaths,
                name=city['nome'],
                code=city['cod'],
                state=state,
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
