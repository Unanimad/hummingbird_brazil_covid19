from django.db import models

import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi


class Kaggle(models.Model):
    last_update = models.DateTimeField(auto_now=False)

    def update_kaggle(self, folder, last_report):
        self.last_update = last_report
        self.save()

        api = KaggleApi()
        api.authenticate()

        api.dataset_create_version(folder, f"Auto update - {last_report}",
                                   delete_old_versions=True)


class Report(models.Model):
    updated_at = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.updated_at.strftime('%d/%m/%Y')


def to_csv():
    df = pd.DataFrame(None, columns=['date', 'hour', 'state',
                                     'suspects', 'refuses', 'cases', 'deaths'])

    df.to_csv('data/brazil_covid19.csv', index=False)


class Case(models.Model):
    STATES = [
        (11, 'Rondônia'), (12, 'Acre'), (13, 'Amazonas'), (14, 'Roraima'),
        (15, 'Pará'), (16, 'Amapá'), (17, 'Tocantins'), (21, 'Maranhão'),
        (22, 'Piauí'), (23, 'Ceará'), (24, 'Rio Grande do Norte'),
        (25, 'Paraíba'), (26, 'Pernambuco'), (27, 'Alagoas'),
        (28, 'Sergipe'), (29, 'Bahia'), (31, 'Minas Gerais'),
        (32, 'Espírito Santo'), (33, 'Rio de Janeiro'), (35, 'São Paulo'),
        (41, 'Paraná'), (42, 'Santa Catarina'), (43, 'Rio Grande do Sul'),
        (50, 'Mato Grosso do Sul'), (51, 'Mato Grosso'), (52, 'Goiás'),
        (53, 'Distrito Federal')
    ]

    state = models.PositiveSmallIntegerField(choices=STATES)

    suspects = models.PositiveSmallIntegerField(default=0)
    refuses = models.PositiveSmallIntegerField(default=0)
    cases = models.PositiveSmallIntegerField(default=0)
    deaths = models.PositiveSmallIntegerField(default=0)

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.state} {self.report}"

    class Meta:
        ordering = ['report', 'state']
        verbose_name = 'Caso'
