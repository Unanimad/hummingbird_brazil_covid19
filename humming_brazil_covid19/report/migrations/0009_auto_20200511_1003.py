# Generated by Django 3.0.4 on 2020-05-11 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_citycase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citycase',
            old_name='city',
            new_name='name',
        ),
    ]
