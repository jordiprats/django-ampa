# Generated by Django 3.1.5 on 2021-11-06 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0042_mailing_representants'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='nomes_representants',
            field=models.BooleanField(default=False),
        ),
    ]
