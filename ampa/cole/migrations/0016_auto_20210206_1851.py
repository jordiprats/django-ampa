# Generated by Django 3.1.5 on 2021-02-06 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cole', '0015_auto_20210206_1845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classe',
            options={'ordering': ['etapa', 'nom']},
        ),
    ]
