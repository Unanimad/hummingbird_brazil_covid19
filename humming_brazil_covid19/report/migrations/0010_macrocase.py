# Generated by Django 3.0.4 on 2020-05-12 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0009_auto_20200511_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='MacroCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cases', models.PositiveIntegerField(default=0)),
                ('deaths', models.PositiveIntegerField(default=0)),
                ('recovered', models.PositiveIntegerField(default=0)),
                ('monitoring', models.PositiveIntegerField(default=0)),
                ('week', models.PositiveSmallIntegerField(default=0)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.Report')),
            ],
        ),
    ]
