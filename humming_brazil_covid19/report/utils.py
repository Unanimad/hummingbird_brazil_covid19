import pandas as pd

from humming_brazil_covid19.report.models import *


def to_csv():
    values = []
    STATES = dict(Case.STATES)
    REGION = dict(Case.REGION)
    columns = [
        'date', 'region', 'state', 'cases', 'deaths'
    ]

    df = pd.DataFrame(None, columns=columns)

    cases = Case.objects.all()

    for case in cases:
        date = datetime.strftime(case.report.updated_at, '%Y-%m-%d')
        region = REGION[case.region]
        state = STATES[case.state]
        cases = case.cases
        deaths = case.deaths

        values.append(dict(zip(columns, [date, region, state, cases, deaths])))

    df = df.append(values, ignore_index=True)
    df = df.sort_values(by=['date', 'region', 'state'])
    df.to_csv('data/brazil_covid19.csv', index=False, columns=columns)
