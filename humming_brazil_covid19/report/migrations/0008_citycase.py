# Generated by Django 3.0.4 on 2020-05-11 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0007_auto_20200506_0930'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('RO', 'Rondônia'), ('AC', 'Acre'), ('AM', 'Amazonas'), ('RR', 'Roraima'), ('PA', 'Pará'), ('AP', 'Amapá'), ('TO', 'Tocantins'), ('MA', 'Maranhão'), ('PI', 'Piauí'), ('CE', 'Ceará'), ('RN', 'Rio Grande do Norte'), ('PB', 'Paraíba'), ('PE', 'Pernambuco'), ('AL', 'Alagoas'), ('SE', 'Sergipe'), ('BA', 'Bahia'), ('MG', 'Minas Gerais'), ('ES', 'Espírito Santo'), ('RJ', 'Rio de Janeiro'), ('SP', 'São Paulo'), ('PR', 'Paraná'), ('SC', 'Santa Catarina'), ('RS', 'Rio Grande do Sul'), ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('GO', 'Goiás'), ('DF', 'Distrito Federal')], max_length=2)),
                ('city', models.TextField()),
                ('code', models.PositiveIntegerField()),
                ('cases', models.PositiveIntegerField(default=0)),
                ('deaths', models.PositiveIntegerField(default=0)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.Report')),
            ],
        ),
    ]