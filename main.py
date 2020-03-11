import json

import requests
import pandas as pd

from datetime import datetime

from utils import *

url = "http://plataforma.saude.gov.br/novocoronavirus/resources/scripts/database.js"

STATES = {11: 'Rondônia', 12: 'Acre', 13: 'Amazonas', 14: 'Roraima', 15: 'Pará',
          16: 'Amapá', 17: 'Tocantins', 21: 'Maranhão', 22: 'Piauí', 23: 'Ceará',
          24: 'Rio Grande do Norte', 25: 'Paraíba', 26: 'Pernambuco', 27: 'Alagoas',
          28: 'Sergipe', 29: 'Bahia', 31: 'Minas Gerais', 32: 'Espírito Santo',
          33: 'Rio de Janeiro', 35: 'São Paulo', 41: 'Paraná', 42: 'Santa Catarina',
          43: 'Rio Grande do Sul', 50: 'Mato Grosso do Sul', 51: 'Mato Grosso',
          52: 'Goiás', 53: 'Distrito Federal'}


def job():
    print("Cron job is running. The time is %s" % datetime.now())
    request = requests.get(url)

    content = request.content.decode('utf8').replace('var database=', '')
    data = json.loads(content)

    df = pd.DataFrame(None, columns=['date', 'hour', 'state',
                                     'suspects', 'refuses', 'cases'])

    for record in data['brazil']:
        confirmed_at = datetime.strptime(record['date'], '%d/%m/%Y')
        confirmed_at = datetime.strftime(confirmed_at, '%Y-%m-%d')
        hour = record['time']

        for value in record['values']:
            state = STATES[int(value['uid'])]

            suspects = get_key_value('suspects', value)
            refuses = get_key_value('refuses', value)
            cases = get_key_value('cases', value)

            df = df.append(dict(zip(df.columns, [confirmed_at, hour, state, suspects, refuses, cases])),
                           ignore_index=True)

    df.to_csv('data/brazil_covid19.csv', index=False, sep=';')
    print("Done! The time is: %s" % datetime.now())
