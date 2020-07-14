import json

import pandas as pd
import requests
from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.models import *

url = "https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/"
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-parse-application-id": "unAFkcaNDeXajurGB7LChj8SgQYS2ptm"
}


def split_database(*args, **options):
    print(f"Job is running. The time is {datetime.now()}")

    request = requests.get(url + "PortalGeral", headers=headers)
    content = request.content.decode("utf8")
    data = json.loads(content)["results"][0]

    xlsx_file = data['arquivo']['url']

    if 'HOJE' in xlsx_file:
        return 'Database inválida'

    df = pd.read_excel(xlsx_file)
    df = df.rename(columns={
        'regiao': 'region', 'estado': 'state', 'municipio': 'name', 'codmun': 'code', 'data': 'date',
        'semanaEpi': 'week', 'casosAcumulado': 'cases', 'obitosAcumulado': 'deaths', 'Recuperadosnovos': 'recovered',
        'emAcompanhamentoNovos': 'monitoring'
    })

    temp = df.loc[df['region'] == 'Brasil']
    temp = temp.rename(columns={'region': 'country'})
    temp = temp.sort_values(by=['date', 'country', 'week'])
    columns = ['date', 'country', 'week', 'cases', 'deaths', 'recovered', 'monitoring']
    temp.to_csv('data/brazil_covid19_macro.csv', index=False, columns=columns)

    temp = df.loc[
        (df['state'].notnull()) &
        (df['name'].isna()) &
        (df['populacaoTCU2019'].notnull())
        ]
    temp = temp.sort_values(by=['date', 'region', 'state'])
    columns = ['date', 'region', 'state', 'cases', 'deaths']
    temp.to_csv('data/brazil_covid19.csv', index=False, columns=columns)

    temp = df.loc[df['name'].notnull()]
    temp = temp.sort_values(by=['date', 'state', 'code'])
    columns = ['date', 'state', 'name', 'code', 'cases', 'deaths']
    temp.to_csv('data/brazil_covid19_cities.csv', index=False, columns=columns)


class Command(BaseCommand):
    help = 'Automatically load the database with the cases of COVID-19 in Brazil.'

    def handle(self, *args, **options):
        split_database()
